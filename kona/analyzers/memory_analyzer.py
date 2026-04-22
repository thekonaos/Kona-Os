from __future__ import annotations

SUCCESS_PATTERNS = {
    "strong_lp": lambda p: p.lp_locked_pct >= 80,
    "no_mint": lambda p: p.mint_disabled,
    "audited": lambda p: p.audit_passed,
    "age_ok": lambda p: p.token_age_days >= 7,
    "distributed": lambda p: p.top10_pct <= 40,
    "has_narrative": lambda p: len(p.narratives) > 0,
    "price_history": lambda p: len(p.price_series) >= 3,
    "holder_growth": lambda p: len(p.holder_series) >= 2 and p.holder_series[-1] > p.holder_series[0],
}


def analyze(token_process) -> float:
    if not token_process:
        return 50.0
    matched = sum(1 for fn in SUCCESS_PATTERNS.values() if fn(token_process))
    total = len(SUCCESS_PATTERNS)
    base = matched / total * 100
    bonus = 0.0
    if token_process.lp_locked_pct >= 95 and token_process.mint_disabled:
        bonus += 8.0
    if token_process.audit_passed and token_process.token_age_days >= 14:
        bonus += 7.0
    return max(0.0, min(100.0, base + bonus))
