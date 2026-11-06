"""Tests must never manufacture a mathematical proof or weaken the regression gate."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r17r1_historical_test_contract.patch import (
    NEW_PARAMS, NEW_TEST, OLD_PARAMS, NEXT_FUNCTION, transform,
)


def fixture() -> str:
    return (
        '"""Sample module."""\nimport pytest\n\n' + OLD_PARAMS + '\n'
        'def test_real_typed_pending_goals_are_grouped_only_in_public_display(n, k, expected):\n'
        '    assert n == n\n'
        + NEXT_FUNCTION + '    assert True\n'
    )


def test_only_historical_parameter_expectation_changes() -> None:
    original = fixture()
    corrected = transform(original)
    ast.parse(corrected)
    assert OLD_PARAMS not in corrected
    assert corrected.count(NEW_PARAMS) == 1
    assert corrected.count("def test_pi8_5_completed_case_is_not_reported_as_an_open_goal") == 1
    assert "assert result.status is ProofSearchStatus.COMPLETE" in corrected
    assert "assert result.open_goals == ()" in corrected
    assert "assert view.key == \"generic-complete-proof\"" in corrected
    assert corrected.count("def test_real_typed_pending_goals_are_grouped_only_in_public_display") == 1
    assert NEW_TEST in corrected


def test_no_repeat_or_unreviewed_changes() -> None:
    corrected = transform(fixture())
    with pytest.raises(RuntimeError):
        transform(corrected)
    with pytest.raises(RuntimeError):
        transform(fixture().replace(OLD_PARAMS, OLD_PARAMS + "\n" + OLD_PARAMS))
    with pytest.raises(RuntimeError):
        transform(fixture().replace(NEXT_FUNCTION, "\n\ndef test_different() -> None:\n"))


def test_new_complete_case_is_not_a_skipped_regression() -> None:
    assert "@pytest.mark.skip" not in NEW_TEST
    assert "pytest.xfail" not in NEW_TEST
    assert "5, k=3" in NEW_TEST
    assert "build_standard_web_group_proof_view" in NEW_TEST
    assert "project_typed_open_goal_displays" in NEW_TEST
