"""Pure policy tests; no application source or real proof state is changed."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase169_r10ed_direct_sum_generality_audit.profile import (
    CASES, AuditCase, validate_coverage,
)


def test_r10ed_case_coverage_includes_two_stems_two_ranks_and_five_lengths():
    validate_coverage(CASES)
    assert {case.k for case in CASES} == {8, 9}
    assert {case.expected_summands for case in CASES} == {2, 3}
    assert {case.expected_suspensions for case in CASES} == {2, 4, 5, 13, 19}
    assert len({(case.n, case.k) for case in CASES}) == 5


def test_r10ed_rejects_narrow_or_duplicate_coverage():
    with pytest.raises(ValueError, match="two different stems"):
        validate_coverage(tuple(c for c in CASES if c.k == 9))
    with pytest.raises(ValueError, match="different direct-sum ranks"):
        validate_coverage(tuple(replace(c, expected_summands=3) for c in CASES))
    with pytest.raises(ValueError, match="distinct"):
        validate_coverage(CASES + (CASES[0],))


def test_r10ed_rejects_invalid_coverage_dimensions():
    with pytest.raises(ValueError, match="invalid dimensions"):
        validate_coverage((replace(CASES[0], expected_suspensions=1),) + CASES[1:])
    with pytest.raises(ValueError, match="invalid dimensions"):
        validate_coverage((replace(CASES[0], expected_summands=1),) + CASES[1:])
    with pytest.raises(ValueError, match="invalid dimensions"):
        validate_coverage((AuditCase(13, 9, True, 3),) + CASES[1:])
