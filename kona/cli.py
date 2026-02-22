from __future__ import annotations
from kona.engine import KonaEngine
from kona.models import TokenProcess, OsVerdict

_COLORS = {
    OsVerdict.KERNEL:  "\033[92m",
    OsVerdict.ROOT:    "\033[32m",
    OsVerdict.SYSTEM:  "\033[33m",
    OsVerdict.USER:    "\033[93m",
    OsVerdict.IDLE:    "\033[90m",
    OsVerdict.CRASHED: "\033[91m",
}
_RESET = "\033[0m"


def _bar(value: float, width: int = 20) -> str:
    filled = int(value / 100 * width)
    return "█" * filled + "░" * (width - filled)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Kona Os — Solana token kernel analyzer")
    parser.add_argument("contract", help="Token contract address")
    parser.add_argument("--lp", type=float, default=0.0, help="LP locked %")
    parser.add_argument("--age", type=int, default=0, help="Token age in days")
    parser.add_argument("--narrative", nargs="*", default=[], help="Narrative text")
    parser.add_argument("--mint-disabled", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()

    engine = KonaEngine()
    token = TokenProcess(
        contract_address=args.contract,
        narratives=args.narrative,
        lp_locked_pct=args.lp,
        mint_disabled=args.mint_disabled,
        audit_passed=args.audit,
        token_age_days=args.age,
    )
    report = engine.analyze(token)
    color = _COLORS.get(report.verdict, "")
    score = report.metrics.final_score()

    print(f"\n{'─'*52}")
    print(f"  Kona Os — Process Report")
    print(f"  PID: {report.process_id} · {token.contract_address[:16]}...")
    print(f"{'─'*52}")
    print(f"  Verdict  : {color}{report.verdict.value}{_RESET}")
    print(f"  Score    : {score:.1f}/100  Uptime: {report.uptime_score:.0f}%")
    print()
    print(f"  {'Signal Clarity':<22} {_bar(report.metrics.signal_clarity)} {report.metrics.signal_clarity:.1f}")
    print(f"  {'Process Health':<22} {_bar(report.metrics.process_health)} {report.metrics.process_health:.1f}")
    print(f"  {'Kernel Stability':<22} {_bar(report.metrics.kernel_stability)} {report.metrics.kernel_stability:.1f}")
    print(f"  {'Routing Efficiency':<22} {_bar(report.metrics.routing_efficiency)} {report.metrics.routing_efficiency:.1f}")
    print(f"  {'Memory Score':<22} {_bar(report.metrics.memory_score)} {report.metrics.memory_score:.1f}")
    print()
    for line in report.log:
        print(f"  {line}")
    print(f"{'─'*52}\n")
