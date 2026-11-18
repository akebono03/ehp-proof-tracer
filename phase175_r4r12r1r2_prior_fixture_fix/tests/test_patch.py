"""Focused regression tests for the previous-report test fixture correction."""
from __future__ import annotations

import pytest

from phase175_r4r12r1r2_prior_fixture_fix.patch import (
    CURRENT_HEAD,
    NEW_FIXTURE,
    OLD_FIXTURE,
    PRIOR_REPORT_HEAD,
    patch_fixture,
)


SOURCE = '''def prior_success_report():
    return {
        "preflight": {"head": audit.HEAD},
        "public": {},
    }


def test_prior_success_is_not_a_root_proof_certificate():
    result = audit.validate_prior(prior_success_report())
    assert result["r4r11_success_verified"] is True
'''


def test_prior_fixture_is_fixed_without_changing_root_test() -> None:
    result = patch_fixture(SOURCE)
    assert NEW_FIXTURE in result
    assert OLD_FIXTURE not in result
    assert 'test_prior_success_is_not_a_root_proof_certificate' in result
    assert 'audit.validate_prior(prior_success_report())' in result


def test_fixture_correction_is_idempotent() -> None:
    once = patch_fixture(SOURCE)
    assert patch_fixture(once) == once


def test_unreviewed_fixture_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="UNREVIEWED_FIXTURE_BODY"):
        patch_fixture(SOURCE.replace(OLD_FIXTURE, '"preflight": {"head": "0" * 40},'))


def test_unrelated_fixture_function_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="PRIOR_FIXTURE_FUNCTION_MISSING"):
        patch_fixture(SOURCE.replace("def prior_success_report", "def other_report"))


def test_historical_and_current_heads_remain_distinct() -> None:
    assert PRIOR_REPORT_HEAD != CURRENT_HEAD
    assert PRIOR_REPORT_HEAD in NEW_FIXTURE
