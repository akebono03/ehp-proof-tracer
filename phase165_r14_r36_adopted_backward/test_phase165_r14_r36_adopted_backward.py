from dataclasses import replace
from pathlib import Path
import pytest
from phase165_r14_r34_backward_search import pi32_goal
from phase165_r14_r35_leaf_binding import backward_leaf_goals
from phase165_r14_r36_adopted_backward import (
    adopted_leaf_steps, reconstruct_adopted_tex_goal, audit_r36,
)
from proof import ProofRule

TEX = Path(__file__).with_name("toda_51_complete.tex")


def test_nine_frontier_leaves_have_one_step_each():
    steps = adopted_leaf_steps(TEX)
    leaves = backward_leaf_goals(pi32_goal())
    assert len(steps) == len(leaves) == 9
    assert all(sum(step.conclusion == leaf for step in steps) == 1 for leaf in leaves)


def test_two_reviewed_diagonals_are_present():
    steps = adopted_leaf_steps(TEX)
    assert len([step for step in steps if "FreeCyclicGroup" in repr(step.conclusion)
                and "TodaPrimaryGroup" in repr(step.conclusion)]) == 3


def test_one_foundational_step_is_not_toda_source():
    steps = adopted_leaf_steps(TEX)
    assert sum(bool(getattr(step, "foundational_reference", None)) for step in steps) == 1


def test_goal_driven_derivation_is_inference_not_replay():
    steps = adopted_leaf_steps(TEX)
    result = reconstruct_adopted_tex_goal(pi32_goal(), steps)
    assert result.conclusion == pi32_goal()
    assert result.rule is ProofRule.INFERENCE
    assert len(result.premises) == 3


def test_missing_leaf_fails_closed():
    with pytest.raises(ValueError):
        reconstruct_adopted_tex_goal(pi32_goal(), adopted_leaf_steps(TEX)[:-1])


def test_duplicate_leaf_fails_closed():
    steps = adopted_leaf_steps(TEX)
    with pytest.raises(ValueError):
        reconstruct_adopted_tex_goal(pi32_goal(), steps + (steps[0],))


def test_audit_distinguishes_adopted_and_strict():
    report = audit_r36(TEX)
    assert report["all_leaf_goals_resolved_for_adopted_search"]
    assert report["adopted_backward_proof_created"]
    assert not report["strict_registry_proof_created"]
    assert not report["existing_completed_proof_replay_used"]
