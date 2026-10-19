from dataclasses import replace

import pytest

from phase161_r5_backward_proof_reconstruction import (
    phase161_r5_target_goal,
    reconstruct_phase161_r5_goal,
)
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


def _independent_phase59_fixture():
    """Reuse only original input leaves, never phase59 result.steps."""
    data = build_phase59_3_data()
    return data["premise_steps"]


def test_phase161_r5_reconstructs_exact_goal_with_seven_new_inferences():
    leaves = _independent_phase59_fixture()
    result = reconstruct_phase161_r5_goal(phase161_r5_target_goal(), leaves)
    assert result.final_step.conclusion == phase161_r5_target_goal()
    assert result.final_step.rule is ProofRule.INFERENCE
    assert len(result.derived_steps) == 7
    assert result.final_step is result.derived_steps[-1]
    assert all(step.rule is ProofRule.INFERENCE for step in result.derived_steps)
    assert all(step is not leaf for step in result.derived_steps for leaf in leaves)
    assert len(result.final_step.premises) == 2
    assert all(premise.rule is ProofRule.INFERENCE for premise in result.final_step.premises)


def test_phase161_r5_preserves_all_four_independent_exactness_witnesses():
    leaves = _independent_phase59_fixture()
    result = reconstruct_phase161_r5_goal(phase161_r5_target_goal(), leaves)
    exactness = tuple(
        step for step in result.leaf_steps
        if isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    assert len(exactness) == 4
    assert all(step.rule is ProofRule.GIVEN for step in exactness)
    assert set(map(id, exactness)) == set(
        id(step) for step in leaves
        if isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )


def test_phase161_r5_rejects_missing_exactness_without_fabricating_given():
    leaves = _independent_phase59_fixture()
    missing = next(step for step in leaves if isinstance(step.conclusion, TodaProp42ExactnessStatement))
    with pytest.raises(ValueError, match="Missing or ambiguous independent exactness"):
        reconstruct_phase161_r5_goal(
            phase161_r5_target_goal(),
            tuple(step for step in leaves if step is not missing),
        )


def test_phase161_r5_rejects_nonindependent_exactness():
    leaves = _independent_phase59_fixture()
    index = next(i for i, step in enumerate(leaves) if isinstance(step.conclusion, TodaProp42ExactnessStatement))
    replaced = list(leaves)
    replaced[index] = replace(replaced[index], rule=ProofRule.INFERENCE)
    with pytest.raises(ValueError, match="Exactness witnesses must be independently supplied"):
        reconstruct_phase161_r5_goal(phase161_r5_target_goal(), tuple(replaced))


def test_phase161_r5_rejects_missing_literature_evidence():
    leaves = _independent_phase59_fixture()
    only_exactness = tuple(step for step in leaves if isinstance(step.conclusion, TodaProp42ExactnessStatement))
    with pytest.raises(ValueError, match="literature match"):
        reconstruct_phase161_r5_goal(phase161_r5_target_goal(), only_exactness)


def test_phase161_r5_rejects_incorrect_goal():
    leaves = _independent_phase59_fixture()
    with pytest.raises(ValueError, match="supports only"):
        reconstruct_phase161_r5_goal(object(), leaves)
