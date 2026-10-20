"""Focused, read-only checks for R3-T's condition matrix."""
from phase166_r3t_gate_audit.audit import inspect

def test_r3t_gate_report_has_real_pi54_goal():
    report = inspect()
    assert report["goal_count"] >= 1
    assert report["cases"]
    assert all("goal" in case for case in report["cases"])

def test_r3t_gate_report_records_transport_gate_conditions():
    report = inspect()
    for case in report["cases"]:
        assert "match_matrix" in case
        assert "direct_toda45_options" in case
        assert "common_rule_names" in case

def test_r3t_gate_report_does_not_change_production():
    report = inspect()
    assert report["mode"] == "read_only"
    assert report["production_code_modified"] is False
    assert report["full_pytest_run"] is False
