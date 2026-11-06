"""Integration check after the exact guarded production connection only."""
from __future__ import annotations

from phase174_r3_r7_r16_public_ehp_zero_root.audit import inspect_public_root
from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME


def test_zero_root_is_exactly_one_unproved_generic_ehp_branch() -> None:
    status = inspect_public_root()
    assert status["public_root_proposal_count"] == 1
    assert status["public_rule_name"] == RULE_NAME
    assert status["unproved_root_child_count"] == 4
    assert status["root_direct_given"] is False
    assert status["new_group_given"] == 0
    assert status["new_math_rule"] == 0
    assert status["proof_completed_claimed"] is False
    assert status["verified_proof_step_from_candidate"] is False
