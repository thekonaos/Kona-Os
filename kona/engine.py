from __future__ import annotations
import hashlib
from kona.models import TokenProcess, OsMetrics, OsVerdict, KernelReport
from kona.agents.signal_agent import SignalAgent
from kona.agents.kernel_agent import KernelAgent
from kona.analyzers.clarity_analyzer import ClarityAnalyzer
from kona.analyzers.routing_analyzer import RoutingAnalyzer
from kona.analyzers import memory_analyzer


def _classify(score: float) -> OsVerdict:
    if score >= 88:
        return OsVerdict.KERNEL
    if score >= 72:
        return OsVerdict.ROOT
    if score >= 55:
        return OsVerdict.SYSTEM
    if score >= 40:
        return OsVerdict.USER
    if score >= 20:
        return OsVerdict.IDLE
    return OsVerdict.CRASHED


def _pid(contract: str) -> str:
    return hashlib.md5(contract.encode()).hexdigest()[:8].upper()


def _build_log(metrics: OsMetrics, verdict: OsVerdict) -> list[str]:
    log = [
        f"kona::boot > spawning process for {verdict.value}",
        f"kona::signal > clarity={metrics.signal_clarity:.1f}",
        f"kona::kernel > health={metrics.process_health:.1f} stability={metrics.kernel_stability:.1f}",
        f"kona::router > efficiency={metrics.routing_efficiency:.1f}",
        f"kona::mem > pattern_score={metrics.memory_score:.1f}",
        f"kona::verdict > final={metrics.final_score():.2f} → {verdict.value}",
    ]
    weak = metrics.weakest()
    if metrics.final_score() < 72:
        log.append(f"kona::warn > weakest subsystem: {weak}")
    if verdict in (OsVerdict.IDLE, OsVerdict.CRASHED):
        log.append("kona::alert > process flagged for termination")
    return log


class KonaEngine:
    def __init__(self) -> None:
        self.signal_agent = SignalAgent()
        self.kernel_agent = KernelAgent()
        self.clarity_analyzer = ClarityAnalyzer()
        self.routing_analyzer = RoutingAnalyzer()

    def analyze(self, token: TokenProcess) -> KernelReport:
        ai_clarity = self.signal_agent.score(token.narratives)
        text_clarity = self.clarity_analyzer.analyze(token.narratives)
        signal_clarity = round(ai_clarity * 0.6 + text_clarity * 0.4, 2)

        process_health = round(self.kernel_agent.process_health(
            lp_locked_pct=token.lp_locked_pct,
            mint_disabled=token.mint_disabled,
            audit_passed=token.audit_passed,
            top10_pct=token.top10_pct,
            token_age_days=token.token_age_days,
        ), 2)

        kernel_stability = round(
            self.kernel_agent.kernel_stability(token.price_series), 2
        )

        routing_efficiency = round(
            self.routing_analyzer.analyze(token.mention_series, token.holder_series), 2
        )

        memory_score = round(memory_analyzer.analyze(token), 2)

        metrics = OsMetrics(
            signal_clarity=signal_clarity,
            process_health=process_health,
            kernel_stability=kernel_stability,
            routing_efficiency=routing_efficiency,
            memory_score=memory_score,
        )

        verdict = _classify(metrics.final_score())
        pid = _pid(token.contract_address)
        log = _build_log(metrics, verdict)
        uptime = round(min(token.token_age_days / 30 * 100, 100), 2)

        return KernelReport(
            contract_address=token.contract_address,
            metrics=metrics,
            verdict=verdict,
            process_id=pid,
            log=log,
            uptime_score=uptime,
        )
