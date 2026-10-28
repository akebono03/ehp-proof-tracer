"""Focused reporting tests: an incomplete proof is never reclassified."""
from __future__ import annotations

from phase169_r10ee_one_stem_regression_audit.audit import (
    CASES, FROZEN_PHASE168, _text, status_assessment,
)


def _cases(status: str = "complete", trust: str = "PASS") -> list[dict]:
    return [
        {"n": n, "k": k, "status": status, "trust": trust,
         "phase168_step_count_equal": True}
        for n, k in CASES
    ]


def test_r10ee_frozen_baseline_covers_three_one_stem_groups():
    assert FROZEN_PHASE168 == {(2, 1): 18, (3, 1): 25, (4, 1): 10}


def test_r10ee_complete_trusted_baselines_do_not_claim_every_group():
    assert status_assessment(_cases()) == "ONE_STEM_STATUS_STEP_COUNTS_AND_TRUST_MATCH"


def test_r10ee_partial_pi54_blocks_phase_closeout():
    cases = _cases()
    cases[2]["status"] = "partial"
    cases[2]["trust"] = "NOT_APPLICABLE_INCOMPLETE"
    assert status_assessment(cases) == "BLOCKED_ONE_STEM_REGRESSION"


def test_r10ee_trust_failure_blocks_closeout():
    cases = _cases()
    cases[1]["trust"] = "FAIL_UnverifiedProofTree"
    assert status_assessment(cases) == "BLOCKED_ONE_STEM_REGRESSION"


def test_r10ee_missing_case_blocks_closeout():
    assert status_assessment(_cases()[:2]) == "BLOCKED_ONE_STEM_REGRESSION"


def test_r10ee_long_debug_repr_is_bounded():
    rendered = _text("X" * 2500, limit=50)
    assert rendered.endswith(" [truncated]")
    assert len(rendered) < 80


def test_r10ee_changed_step_count_blocks_closeout():
    cases = _cases()
    cases[0]["phase168_step_count_equal"] = False
    assert status_assessment(cases) == "BLOCKED_ONE_STEM_REGRESSION"
