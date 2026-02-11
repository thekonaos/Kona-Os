from __future__ import annotations


PROCESS_HEALTH_WEIGHTS = {
    "lp_locked": 30,
    "mint_disabled": 20,
    "audit_passed": 15,
    "top10_safe": 20,
    "age_bonus": 15,
}


def _lp_score(lp_pct: float) -> float:
    if lp_pct >= 95:
        return 100.0
    if lp_pct >= 80:
        return 80.0
    if lp_pct >= 50:
        return 55.0
    if lp_pct >= 20:
        return 25.0
    return 5.0


def _top10_score(top10_pct: float) -> float:
    if top10_pct <= 20:
        return 100.0
    if top10_pct <= 40:
        return 70.0
    if top10_pct <= 60:
        return 40.0
    if top10_pct <= 80:
        return 15.0
    return 0.0


def _age_score(age_days: int) -> float:
    if age_days >= 30:
        return 100.0
    if age_days >= 14:
        return 70.0
    if age_days >= 7:
        return 45.0
    if age_days >= 3:
        return 25.0
    return 10.0


class KernelAgent:
    def process_health(
        self,
        lp_locked_pct: float,
        mint_disabled: bool,
        audit_passed: bool,
        top10_pct: float,
        token_age_days: int,
    ) -> float:
        lp = _lp_score(lp_locked_pct) * PROCESS_HEALTH_WEIGHTS["lp_locked"] / 100
        mint = PROCESS_HEALTH_WEIGHTS["mint_disabled"] if mint_disabled else 0
        audit = PROCESS_HEALTH_WEIGHTS["audit_passed"] if audit_passed else 0
        top10 = _top10_score(top10_pct) * PROCESS_HEALTH_WEIGHTS["top10_safe"] / 100
        age = _age_score(token_age_days) * PROCESS_HEALTH_WEIGHTS["age_bonus"] / 100
        return max(0.0, min(100.0, lp + mint + audit + top10 + age))

    def kernel_stability(self, price_series: list[float]) -> float:
        if len(price_series) < 2:
            return 50.0
        import statistics
        mean = statistics.mean(price_series) or 1.0
        stdev = statistics.stdev(price_series) if len(price_series) > 1 else 0.0
        cv = stdev / mean
        stability = max(0.0, 100.0 - cv * 120)
        trend = (price_series[-1] - price_series[0]) / (price_series[0] or 1.0) * 100
        trend_bonus = min(max(trend * 0.2, -20), 20)
        return max(0.0, min(100.0, stability + trend_bonus))
