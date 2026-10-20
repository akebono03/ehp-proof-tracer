"""Targeted R3-T diagnostics; no production modifications."""
from audit import inspect


def test_r3t_has_registered_pi54_candidate():
    result = inspect()
    assert result["pi54_candidate_count"] >= 1


def test_r3t_does_not_change_production_code():
    result = inspect()
    assert result["production_code_modified"] is False
    assert result["full_pytest_run"] is False


def test_r3t_web_pi54_result_is_reported():
    result = inspect()
    assert "pi_5^4" in result["web_views"]
