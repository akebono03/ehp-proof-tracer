from dataclasses import replace
from pathlib import Path
import pytest

from phase165_r14_r34_backward_search import pi32_goal, phase165_r34_expansions
from phase165_r14_r38_direct_registry import (
    build_adopted_typed_reference_registry,
    reconstruct_registered_pi32,
    audit_completion,
)
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule

TEX = Path(__file__).with_name("toda_51_complete.tex")


def test_nine_typed_registered_reference_leaves():
    bridge = build_adopted_typed_reference_registry(TEX)
    assert len(bridge.proof_links) == 9
    assert len({link.assertion_id for link in bridge.proof_links}) == 9


def test_registered_goal_driven_proof_created():
    bridge, proof = reconstruct_registered_pi32(TEX)
    assert proof.conclusion == pi32_goal()
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 3


def test_no_separate_approval_list_needed():
    bridge = build_adopted_typed_reference_registry(TEX)
    proof = reconstruct_registered_goal(
        pi32_goal(), bridge, "goal:pi32", phase165_r34_expansions,
        verified_assertion_ids=(), lookup_mode="typed_reference",
    )
    assert proof.conclusion == pi32_goal()


def test_wrong_leaf_conclusion_fails_closed():
    bridge = build_adopted_typed_reference_registry(TEX)
    first = bridge.proof_links[0]
    bad_link = replace(first, step=replace(first.step, conclusion=object()))
    broken = replace(bridge, proof_links=(bad_link,) + bridge.proof_links[1:])
    with pytest.raises((ValueError, RegisteredGoalUnresolved)):
        reconstruct_registered_goal(
            pi32_goal(), broken, "goal:pi32", phase165_r34_expansions,
            lookup_mode="typed_reference",
        )


def test_missing_registered_leaf_fails_closed():
    bridge = build_adopted_typed_reference_registry(TEX)
    broken = replace(bridge, proof_links=bridge.proof_links[:-1])
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            pi32_goal(), broken, "goal:pi32", phase165_r34_expansions,
            lookup_mode="typed_reference",
        )


def test_no_false_original_edition_claim():
    result = audit_completion(TEX)
    assert result["registered_backward_proof_created"]
    assert not result["original_edition_independently_verified"]
