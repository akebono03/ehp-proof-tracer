"""Focused audit tests; no proof search or full test suite."""
from audit import run


def test_112_targets_present():
    report = run()
    assert report["count"] == 112
    assert report["source_counts"].get("missing", 0) == 0


def test_no_suspension_power_one_in_public_goals():
    report = run()
    assert report["issue_counts"].get("unnecessary_E_power_one", 0) == 0
