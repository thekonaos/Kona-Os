import pytest
from kona.models import TokenProcess, OsMetrics, OsVerdict, KernelReport


def test_os_verdict_values():
    assert OsVerdict.KERNEL == "KERNEL"
    assert OsVerdict.CRASHED == "CRASHED"
    assert len(OsVerdict) == 6


def test_os_verdict_all_members():
    members = {v.value for v in OsVerdict}
    assert members == {"KERNEL", "ROOT", "SYSTEM", "USER", "IDLE", "CRASHED"}


def test_token_process_defaults():
    t = TokenProcess(contract_address="test123")
    assert t.narratives == []
    assert t.price_series == []
    assert t.holder_series == []
    assert t.lp_locked_pct == 0.0
    assert t.mint_disabled is False
    assert t.audit_passed is False
    assert t.token_age_days == 0


def test_token_process_empty_address_normalized():
    t = TokenProcess(contract_address="")
    assert t.contract_address == "unknown"


def test_os_metrics_final_score_weights():
    m = OsMetrics(100.0, 0.0, 0.0, 0.0, 0.0)
    assert m.final_score() == pytest.approx(25.0)


def test_os_metrics_process_health_weight():
    m = OsMetrics(0.0, 100.0, 0.0, 0.0, 0.0)
    assert m.final_score() == pytest.approx(25.0)


def test_os_metrics_full_score():
    m = OsMetrics(100.0, 100.0, 100.0, 100.0, 100.0)
    assert m.final_score() == pytest.approx(100.0)


def test_os_metrics_weakest():
    m = OsMetrics(80.0, 80.0, 80.0, 10.0, 80.0)
    assert m.weakest() == "routing_efficiency"


def test_os_metrics_dominant():
    m = OsMetrics(20.0, 20.0, 20.0, 95.0, 20.0)
    assert m.dominant() == "routing_efficiency"


def test_kernel_report_fields():
    m = OsMetrics(70.0, 70.0, 70.0, 70.0, 70.0)
    r = KernelReport(
        contract_address="test",
        metrics=m,
        verdict=OsVerdict.ROOT,
        process_id="DEADBEEF",
        log=["boot ok"],
        uptime_score=80.0,
    )
    assert r.verdict == OsVerdict.ROOT
    assert r.process_id == "DEADBEEF"
    assert r.uptime_score == 80.0


def test_kernel_report_defaults():
    m = OsMetrics(50.0, 50.0, 50.0, 50.0, 50.0)
    r = KernelReport(contract_address="x", metrics=m, verdict=OsVerdict.USER, process_id="AA")
    assert r.log == []
    assert r.uptime_score == 0.0
