"""Phase 161 R6: independent focused audits of R5 reconstruction contracts."""

from dataclasses import replace

import pytest

from phase161_r5_backward_proof_reconstruction import (
    phase161_r5_target_goal,
    reconstruct_phase161_r5_goal,
)
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


@pytest.fixture(scope="module")
def phase161_r6_leaves():
    return build_phase59_3_data()["premise_steps"]


def test_phase161_r6_seven_derived_steps_form_ancestry(phase161_r6_leaves):
    result = reconstruct_phase161_r5_goal(
        phase161_r5_target_goal(), phase161_r6_leaves
    )
    derived_ids = {id(step) for step in result.derived_steps}
    leaf_ids = {id(step) for step in result.leaf_steps}
    assert len(derived_ids) == 7
    assert derived_ids.isdisjoint(leaf_ids)
    assert result.final_step is result.derived_steps[-1]
    assert result.final_step.conclusion == result.goal
    assert all(step.rule is ProofRule.INFERENCE for step in result.derived_steps)
    assert all(step.inference_rule is not None for step in result.derived_steps)
    reachable = set()

    def visit(step):
        if id(step) in reachable:
            return
        reachable.add(id(step))
        for premise in step.premises:
            assert isinstance(premise, ProofStep)
            visit(premise)

    visit(result.final_step)
    assert derived_ids.issubset(reachable)
    assert leaf_ids.issubset(reachable)


def test_phase161_r6_each_exactness_is_necessary(phase161_r6_leaves):
    exactness = tuple(
        step for step in phase161_r6_leaves
        if isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    assert len(exactness) == 4
    for missing in exactness:
        subset = tuple(step for step in phase161_r6_leaves if step is not missing)
        with pytest.raises(ValueError, match="Missing or ambiguous independent exactness"):
            reconstruct_phase161_r5_goal(phase161_r5_target_goal(), subset)


def test_phase161_r6_each_literature_witness_is_necessary(phase161_r6_leaves):
    literature = tuple(
        step for step in phase161_r6_leaves
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    assert len(literature) == 2
    for missing in literature:
        subset = tuple(step for step in phase161_r6_leaves if step is not missing)
        with pytest.raises(ValueError, match="literature match"):
            reconstruct_phase161_r5_goal(phase161_r5_target_goal(), subset)


def test_phase161_r6_records_unverified_literature_ancestry_boundary(phase161_r6_leaves):
    literature = next(
        step for step in phase161_r6_leaves
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    ungrounded = replace(literature, premises=())
    assert ungrounded.rule is ProofRule.INFERENCE
    assert ungrounded.premises == ()
    subset = tuple(ungrounded if step is literature else step for step in phase161_r6_leaves)
    result = reconstruct_phase161_r5_goal(phase161_r5_target_goal(), subset)
    assert result.final_step.conclusion == result.goal
    assert any(step is ungrounded for step in result.leaf_steps)
