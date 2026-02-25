import pytest
from kona.agents.signal_agent import SignalAgent, _heuristic_clarity
from kona.agents.kernel_agent import KernelAgent, _lp_score, _top10_score, _age_score


# --- SignalAgent / heuristic ---

def test_heuristic_empty():
    assert _heuristic_clarity([]) == 50.0


def test_heuristic_clean_narrative():
    score = _heuristic_clarity([
        "community locked liquidity audit doxxed roadmap building partnership organic staking"
    ])
    assert score > 50.0


def test_heuristic_pure_noise():
    score = _heuristic_clarity(["moon ape wagmi 100x fomo pump send degen chad"])
    assert 0.0 <= score <= 100.0


def test_heuristic_crash_signals():
    score = _heuristic_clarity(["rug scam honeypot drain exit dump bot abandoned"])
    assert score < 30.0


def test_heuristic_bounds():
    score = _heuristic_clarity(["some random narrative text about solana"])
    assert 0.0 <= score <= 100.0


def test_signal_agent_no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    agent = SignalAgent()
    score = agent.score(["community locked liquidity building"])
    assert 0.0 <= score <= 100.0


# --- KernelAgent / helpers ---

def test_lp_score_full_lock():
    assert _lp_score(100.0) == 100.0


def test_lp_score_no_lock():
    assert _lp_score(0.0) == 5.0


def test_lp_score_mid():
    score = _lp_score(60.0)
    assert 40.0 <= score <= 70.0


def test_top10_score_distributed():
    assert _top10_score(15.0) == 100.0


def test_top10_score_concentrated():
    assert _top10_score(90.0) == 0.0


def test_age_score_old():
    assert _age_score(60) == 100.0


def test_age_score_new():
    assert _age_score(1) == 10.0


def test_kernel_agent_process_health_perfect():
    agent = KernelAgent()
    score = agent.process_health(
        lp_locked_pct=95.0,
        mint_disabled=True,
        audit_passed=True,
        top10_pct=15.0,
        token_age_days=30,
    )
    assert score >= 90.0


def test_kernel_agent_process_health_worst():
    agent = KernelAgent()
    score = agent.process_health(
        lp_locked_pct=0.0,
        mint_disabled=False,
        audit_passed=False,
        top10_pct=95.0,
        token_age_days=0,
    )
    assert score <= 15.0


def test_kernel_stability_flat():
    score = KernelAgent().kernel_stability([0.01, 0.01, 0.01, 0.01])
    assert score >= 80.0


def test_kernel_stability_volatile():
    score = KernelAgent().kernel_stability([0.01, 0.05, 0.002, 0.08, 0.001])
    assert score < 60.0


def test_kernel_stability_single_point():
    assert KernelAgent().kernel_stability([0.01]) == 50.0


def test_kernel_stability_empty():
    assert KernelAgent().kernel_stability([]) == 50.0
