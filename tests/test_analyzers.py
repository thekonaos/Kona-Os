import pytest
from kona.analyzers.clarity_analyzer import ClarityAnalyzer
from kona.analyzers.routing_analyzer import RoutingAnalyzer
from kona.analyzers import memory_analyzer
from kona.models import TokenProcess


# --- ClarityAnalyzer ---

def test_clarity_empty():
    assert ClarityAnalyzer().analyze([]) == 50.0


def test_clarity_technical_terms_boost():
    score_tech = ClarityAnalyzer().analyze(["tokenomics vesting multisig dao governance staking yield"])
    score_plain = ClarityAnalyzer().analyze(["this is a token on solana"])
    assert score_tech >= score_plain


def test_clarity_meme_quality_boost():
    score = ClarityAnalyzer().analyze(["original unique culture community viral narrative brand niche"])
    assert score > 40.0


def test_clarity_diverse_vocab_boost():
    diverse = ClarityAnalyzer().analyze(["tokenomics vesting multisig dao governance staking yield apy tvl dex"])
    repetitive = ClarityAnalyzer().analyze(["moon moon moon moon moon moon moon moon moon moon"])
    assert diverse > repetitive


def test_clarity_bounds():
    score = ClarityAnalyzer().analyze(["random text for solana token project"])
    assert 0.0 <= score <= 100.0


# --- RoutingAnalyzer ---

def test_routing_empty_series():
    score = RoutingAnalyzer().analyze([], [])
    assert 0.0 <= score <= 100.0


def test_routing_growing_mentions():
    score = RoutingAnalyzer().analyze([100.0, 200.0, 400.0, 800.0], [100, 200, 400])
    assert score > 50.0


def test_routing_declining_mentions():
    score = RoutingAnalyzer().analyze([1000.0, 500.0, 200.0, 50.0], [5000, 3000, 1000])
    assert score <= 60.0


def test_routing_single_point():
    score = RoutingAnalyzer().analyze([100.0], [200])
    assert 0.0 <= score <= 100.0


def test_routing_bounds():
    score = RoutingAnalyzer().analyze([10.0, 1000.0], [10, 10000])
    assert 0.0 <= score <= 100.0


# --- MemoryAnalyzer ---

def test_memory_none_input():
    assert memory_analyzer.analyze(None) == 50.0


def test_memory_healthy_token(healthy_token):
    score = memory_analyzer.analyze(healthy_token)
    assert score > 60.0


def test_memory_crashed_token(crashed_token):
    score = memory_analyzer.analyze(crashed_token)
    assert score < 40.0


def test_memory_basic_token(basic_token):
    score = memory_analyzer.analyze(basic_token)
    assert 0.0 <= score <= 100.0


def test_memory_bonus_for_full_lock():
    t = TokenProcess(
        contract_address="bonus_test",
        lp_locked_pct=97.0,
        mint_disabled=True,
        audit_passed=True,
        token_age_days=30,
        top10_pct=15.0,
        narratives=["community building"],
        price_series=[0.01, 0.012, 0.015],
        holder_series=[100, 200, 350],
    )
    score = memory_analyzer.analyze(t)
    assert score > 80.0


def test_memory_bounds(healthy_token, crashed_token):
    for t in [healthy_token, crashed_token]:
        s = memory_analyzer.analyze(t)
        assert 0.0 <= s <= 100.0
