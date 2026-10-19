from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase162_group_structure_backward import (
    expand_group_structure_goal,
    reconstruct_group_structure_goal,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data


def _fixture():
    eta2_squared = HomotopyElement(name="η₂²", dimension=4, source=4, target=2, generator=GeneratorSymbol(family="η", index=2))
    eta3_squared = HomotopyElement(name="η₃²", dimension=5, source=5, target=3, generator=GeneratorSymbol(family="η", index=3))
    e = TodaSuspensionMap(TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3))
    goal = Relation(lhs=e.target_group, rhs=FiniteCyclicGroup(order=2, generator=eta3_squared), relation_type=RelationType.EQUALITY)
    plan = expand_group_structure_goal(goal, e, eta2_squared)
    group_leaves = (
        ProofStep(conclusion=plan.source_structure_goal, premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=plan.generator_image_goal, premises=(), rule=ProofRule.GIVEN),
    )
    return goal, e, eta2_squared, group_leaves


def test_phase162_goal_first_transport_uses_existing_seven_steps():
    goal, e, generator, group_leaves = _fixture()
    ehp = build_phase59_3_data()["premise_steps"]
    result = reconstruct_group_structure_goal(goal, e, generator, ehp, group_leaves)
    assert result.goal == goal
    assert result.final_step.conclusion == goal
    assert result.final_step.rule is ProofRule.INFERENCE
    assert len(result.derived_steps) == 8
    assert result.final_step is result.derived_steps[-1]
    assert result.final_step.premises[0] is result.derived_steps[-2]
    assert result.final_step.premises[1:] == group_leaves
    assert result.plan.expansion.goal == goal
    assert len(result.plan.expansion.subgoals) == 3


def test_phase162_missing_source_structure_fails():
    goal, e, generator, group_leaves = _fixture()
    with pytest.raises(ValueError, match="Missing or ambiguous independent group premise"):
        reconstruct_group_structure_goal(goal, e, generator, build_phase59_3_data()["premise_steps"], group_leaves[1:])


def test_phase162_missing_generator_image_fails():
    goal, e, generator, group_leaves = _fixture()
    with pytest.raises(ValueError, match="Missing or ambiguous independent group premise"):
        reconstruct_group_structure_goal(goal, e, generator, build_phase59_3_data()["premise_steps"], group_leaves[:1])


def test_phase162_wrong_generator_image_fails():
    goal, e, generator, group_leaves = _fixture()
    wrong = replace(group_leaves[1], conclusion=replace(group_leaves[1].conclusion, rhs=generator))
    with pytest.raises(ValueError, match="Missing or ambiguous independent group premise"):
        reconstruct_group_structure_goal(goal, e, generator, build_phase59_3_data()["premise_steps"], (group_leaves[0], wrong))


def test_phase162_wrong_source_group_fails():
    goal, e, generator, group_leaves = _fixture()
    wrong = replace(group_leaves[0], conclusion=replace(group_leaves[0].conclusion, lhs=TodaPrimaryGroup(3, 2)))
    with pytest.raises(ValueError, match="Missing or ambiguous independent group premise"):
        reconstruct_group_structure_goal(goal, e, generator, build_phase59_3_data()["premise_steps"], (wrong, group_leaves[1]))


def test_phase162_transport_rejects_unrelated_goal():
    goal, e, generator, _ = _fixture()
    with pytest.raises(ValueError, match="target finite cyclic group"):
        expand_group_structure_goal(replace(goal, lhs=TodaPrimaryGroup(6, 3)), e, generator)
