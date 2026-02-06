from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class OsVerdict(str, Enum):
    KERNEL = "KERNEL"
    ROOT = "ROOT"
    SYSTEM = "SYSTEM"
    USER = "USER"
    IDLE = "IDLE"
    CRASHED = "CRASHED"


@dataclass
class TokenProcess:
    contract_address: str
    narratives: list[str] = field(default_factory=list)
    price_series: list[float] = field(default_factory=list)
    holder_series: list[int] = field(default_factory=list)
    lp_locked_pct: float = 0.0
    mint_disabled: bool = False
    audit_passed: bool = False
    top10_pct: float = 0.0
    token_age_days: int = 0
    mention_series: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.contract_address:
            self.contract_address = "unknown"


@dataclass
class OsMetrics:
    signal_clarity: float
    process_health: float
    kernel_stability: float
    routing_efficiency: float
    memory_score: float

    def final_score(self) -> float:
        return (
            self.signal_clarity * 0.25
            + self.process_health * 0.25
            + self.kernel_stability * 0.20
            + self.routing_efficiency * 0.20
            + self.memory_score * 0.10
        )

    def weakest(self) -> str:
        axes = {
            "signal_clarity": self.signal_clarity,
            "process_health": self.process_health,
            "kernel_stability": self.kernel_stability,
            "routing_efficiency": self.routing_efficiency,
            "memory_score": self.memory_score,
        }
        return min(axes, key=lambda k: axes[k])

    def dominant(self) -> str:
        axes = {
            "signal_clarity": self.signal_clarity,
            "process_health": self.process_health,
            "kernel_stability": self.kernel_stability,
            "routing_efficiency": self.routing_efficiency,
            "memory_score": self.memory_score,
        }
        return max(axes, key=lambda k: axes[k])


@dataclass
class KernelReport:
    contract_address: str
    metrics: OsMetrics
    verdict: OsVerdict
    process_id: str
    log: list[str] = field(default_factory=list)
    uptime_score: float = 0.0
