"""No production imports required for safe matcher-diagnostic classifier tests."""
from __future__ import annotations

import pytest

from phase173_r4_r1_root_match_probe.audit import (
    only_audit_additions, summarize_premise_states,
)


def test_all_accepted_no_match_is_rejected() -> None:
    assert summarize_premise_states(("ACCEPTED",) * 4, 0) == (
        "MATCHER_REJECTED_FOUR_ACCEPTED_PREMISES"
    )


def test_all_accepted_matching_rule_is_not_proof_certified() -> None:
    assert summarize_premise_states(("ACCEPTED",) * 4, 1) == (
        "MATCHED_PROOF_NOT_COMPLETED"
    )


def test_missing_premise_does_not_suggest_matcher_failure() -> None:
    assert summarize_premise_states(("ACCEPTED", "MISSING", "ACCEPTED", "ACCEPTED"), None) == (
        "MISSING_ACCEPTED_PREMISE"
    )


def test_wrong_proof_rule_is_reported() -> None:
    assert summarize_premise_states(("ACCEPTED", "WRONG_RULE", "ACCEPTED", "ACCEPTED"), None) == (
        "WRONG_PROOF_RULE"
    )


def test_ambiguous_steps_are_reported() -> None:
    assert summarize_premise_states(("ACCEPTED", "AMBIGUOUS", "ACCEPTED", "ACCEPTED"), None) == (
        "AMBIGUOUS_ACCEPTED_STEPS"
    )


def test_wrong_number_of_premises_fails_closed() -> None:
    with pytest.raises(ValueError):
        summarize_premise_states(("ACCEPTED",) * 3, 1)


def test_bad_number_of_matches_fails_closed() -> None:
    with pytest.raises(ValueError):
        summarize_premise_states(("ACCEPTED",) * 4, 2)


def test_only_audit_additions_allowed() -> None:
    assert only_audit_additions(
        "A\tphase173_r4_r1_sample/audit.py\nA\tphase173_r4_r1_sample/tests/test_audit.py"
    ) == ("phase173_r4_r1_sample/audit.py", "phase173_r4_r1_sample/tests/test_audit.py")


@pytest.mark.parametrize("changes", [
    "M\tphase165_r52_r9_shared_math.py",
    "D\tphase173_r4_r1_sample/audit.py",
    "A\tphase165_new/unsafe.py",
    "A\tREADME.md",
    "A\tphase173_r4_r1_sample/../unsafe.py",
    "A\tphase173_r4_r1_sample\\unsafe.py",
])
def test_reject_non_audit_committed_diff(changes: str) -> None:
    with pytest.raises(RuntimeError):
        only_audit_additions(changes)
