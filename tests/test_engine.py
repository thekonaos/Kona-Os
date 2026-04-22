import pytest
from kona.engine import KonaEngine, _classify, _pid
from kona.models import OsVerdict


def test_classify_kernel():
    assert _classify(90.0) == OsVerdict.KERNEL


def test_classify_root():
    assert _classify(75.0) == OsVerdict.ROOT


def test_classify_system():
    assert _classify(60.0) == OsVerdict.SYSTEM


def test_classify_user():
    assert _classify(45.0) == OsVerdict.USER


def test_classify_idle():
    assert _classify(25.0) == OsVerdict.IDLE


def test_classify_crashed():
    assert _classify(10.0) == OsVerdict.CRASHED


def test_classify_boundary_88():
    assert _classify(88.0) == OsVerdict.KERNEL


def test_classify_boundary_72():
    assert _classify(72.0) == OsVerdict.ROOT


def test_pid_deterministic():
    assert _pid("abc") == _pid("abc")


def test_pid_length():
    assert len(_pid("some_contract_address")) == 8


def test_pid_uppercase():
    pid = _pid("test")
    assert pid == pid.upper()


def test_engine_analyze_basic(basic_token):
    engine = KonaEngine()
    report = engine.analyze(basic_token)
    assert report.verdict in OsVerdict.__members__.values()
    assert 0.0 <= report.metrics.final_score() <= 100.0
    assert len(report.process_id) == 8
    assert len(report.log) > 0


def test_engine_analyze_healthy(healthy_token):
    engine = KonaEngine()
    report = engine.analyze(healthy_token)
    assert report.verdict in {OsVerdict.KERNEL, OsVerdict.ROOT, OsVerdict.SYSTEM}


def test_engine_analyze_crashed(crashed_token):
    engine = KonaEngine()
    report = engine.analyze(crashed_token)
    assert report.verdict in {OsVerdict.USER, OsVerdict.IDLE, OsVerdict.CRASHED}


def test_engine_report_contract(healthy_token):
    engine = KonaEngine()
    report = engine.analyze(healthy_token)
    assert report.contract_address == healthy_token.contract_address


def test_engine_uptime_score_young(basic_token):
    engine = KonaEngine()
    report = engine.analyze(basic_token)
    assert report.uptime_score == 0.0


def test_engine_uptime_score_old(healthy_token):
    engine = KonaEngine()
    report = engine.analyze(healthy_token)
    assert report.uptime_score == pytest.approx(70.0)
