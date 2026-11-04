"""Focused read-only audit tests; no all-suite regression run."""
from __future__ import annotations

import pytest

from phase173_r4_r15r12r3_all_n4_status_audit.audit import (
    classify_observed_status,
    discover_registered_n4,
    make_summary,
)


def test_registered_n4_uses_only_explicit_sphere_csv_rows() -> None:
    discovered = discover_registered_n4()
    assert tuple(discovered) == tuple(range(1, 34))
    assert len(discovered) == 33
    assert len(tuple(k for k in discovered if k >= 8)) == 26
    assert all(discovered[k] for k in discovered)


@pytest.mark.parametrize(
    "search_status,web_key,web_partial,abstract,conclusion,open_goals,expected",
    (
        ("complete", "generic-complete-proof", False, False, True, 0, "NAMED_COMPLETE"),
        ("search_failed", "generic-partial-proof", True, True, False, 3, "ABSTRACT_ONLY_NAMED_PENDING"),
        ("partial", "generic-partial-proof", True, False, False, 2, "NAMED_PENDING_NO_ABSTRACT"),
        ("search_failed", "generic-complete-proof", False, True, False, 3, "INCONSISTENT_SEARCH_WEB"),
        ("complete", "generic-partial-proof", True, False, True, 0, "INCONSISTENT_SEARCH_WEB"),
        ("complete", "generic-complete-proof", False, False, True, 1, "INCONSISTENT_SEARCH_WEB"),
        (None, None, None, False, False, None, "NOT_VERIFIED_ERROR"),
    ),
)
def test_status_contract_never_promotes_unproven_named_generators(
    search_status: str | None,
    web_key: str | None,
    web_partial: bool | None,
    abstract: bool,
    conclusion: bool,
    open_goals: int | None,
    expected: str,
) -> None:
    assert classify_observed_status(
        search_status, web_key, web_partial, abstract, conclusion, open_goals
    ) == expected


def test_summary_keeps_abstract_only_separate_from_named_complete() -> None:
    rows = [
        {"k": 3, "category": "NAMED_COMPLETE", "unsupported_math_line_count": 0, "raw_relation_diagnostic_count": 0, "abstract_input_compatible": True, "named_generator_shape_compatible": True},
        {"k": 8, "category": "ABSTRACT_ONLY_NAMED_PENDING", "unsupported_math_line_count": 1, "raw_relation_diagnostic_count": 1, "abstract_input_compatible": True, "named_generator_shape_compatible": False},
        {"k": 31, "category": "ABSTRACT_ONLY_NAMED_PENDING", "unsupported_math_line_count": 2, "raw_relation_diagnostic_count": 0, "abstract_input_compatible": True, "named_generator_shape_compatible": False},
    ]
    summary = make_summary(rows)
    assert summary["all_status_counts"]["NAMED_COMPLETE"] == 1
    assert summary["k_ge_8_named_complete"] == []
    assert summary["k_ge_8_abstract_only"] == [8, 31]
    assert summary["k_ge_8_unrendered_math"] == [8, 31]
    assert summary["k_ge_8_raw_relation_diagnostics"] == [8]
    assert summary["k_ge_8_abstract_input_shape_eligible"] == [8, 31]
    assert summary["k_ge_8_named_input_shape_eligible"] == []
    assert summary["full_pytest_run"] is False
