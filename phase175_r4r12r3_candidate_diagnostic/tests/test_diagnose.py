"""Focused non-mathematical diagnostic helper tests."""
from __future__ import annotations

from phase175_r4r12r3_candidate_diagnostic.diagnose import equal_check


def test_equal_check_reports_match() -> None:
    result = equal_check("generator", (9, 5), (9, 5))
    assert result["equal"] is True
    assert result["check"] == "generator"


def test_equal_check_reports_mismatch_without_asserting_proof() -> None:
    result = equal_check("generator", (9, 4), (9, 5))
    assert result["equal"] is False
    assert result["actual"] != result["expected"]
