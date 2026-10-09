"""Focused tests for the existing-rule, bounded pi_5^3 backward selection."""

import pytest

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase162_pi5_3_backward_selection import (
    _canonical_goals,
    expand_phase162_pi5_3_group_goal,
    reconstruct_phase162_pi5_3_group_goal,
)
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import toda_eta_family_definition_statement


def _inputs():
    pi4_2 = build_phase59_2_data()["result_steps"][0]
    definitions = tuple(
        ProofStep(conclusion=toda_eta_family_definition_statement(i), premises=(), rule=ProofRule.GIVEN)
        for i in (3, 4)
    )
    ehp_leaves = build_phase59_3_data()["premise_steps"]
    return pi4_2, definitions, ehp_leaves


def test_group_goal_selects_existing_transport_premises():
    pi4_2, goal, bridge = _canonical_goals()
    expansion = expand_phase162_pi5_3_group_goal(goal)
    assert expansion is not None
    assert expansion.goal == goal
    assert expansion.subgoals == (pi4_2, phase161_r5_target_goal(), bridge)
    assert expansion.inference_rule.conclusion_builder is not None


def test_group_goal_reconstruction_uses_new_suspension_step():
    _, goal, _ = _canonical_goals()
    pi4_2, definitions, leaves = _inputs()
    result = reconstruct_phase162_pi5_3_group_goal(goal, pi4_2, definitions, leaves)
    assert result.final_step.conclusion == goal
    assert result.final_step.rule is ProofRule.INFERENCE
    assert result.final_step.premises == (pi4_2, result.suspension_step, result.bridge_step)
    assert result.suspension_step.conclusion == phase161_r5_target_goal()
    assert all(result.suspension_step is not step for step in leaves)
    assert result.bridge_step.premises == definitions
    assert result.final_step not in leaves


def test_group_goal_rejects_unrelated_goal():
    pi4_2, _, _ = _canonical_goals()
    assert expand_phase162_pi5_3_group_goal(pi4_2) is None
    with pytest.raises(ValueError, match="Unsupported group goal"):
        reconstruct_phase162_pi5_3_group_goal(pi4_2, *_inputs())


def test_group_goal_rejects_given_pi4_2_result():
    _, goal, _ = _canonical_goals()
    pi4_2, definitions, leaves = _inputs()
    false_step = ProofStep(conclusion=pi4_2.conclusion, premises=(), rule=ProofRule.GIVEN)
    with pytest.raises(ValueError, match="independently derived pi_4"):
        reconstruct_phase162_pi5_3_group_goal(goal, false_step, definitions, leaves)


def test_group_goal_rejects_unproven_eta_definition():
    _, goal, _ = _canonical_goals()
    pi4_2, definitions, leaves = _inputs()
    bad = ProofStep(conclusion=definitions[0].conclusion, premises=(), rule=ProofRule.INFERENCE)
    with pytest.raises(ValueError, match="eta definition"):
        reconstruct_phase162_pi5_3_group_goal(goal, pi4_2, (bad, definitions[1]), leaves)


def test_group_goal_rejects_missing_ehp_evidence():
    _, goal, _ = _canonical_goals()
    pi4_2, definitions, _ = _inputs()
    with pytest.raises(ValueError):
        reconstruct_phase162_pi5_3_group_goal(goal, pi4_2, definitions, ())


def test_bridge_subgoal_is_existing_rule_conclusion():
    from proof import apply_inference_match, find_inference_matches_for_rule
    from toda_rules import toda_prop53_n3_eta_square_suspension_bridge_inference_rule

    _, _, bridge = _canonical_goals()
    _, definitions, _ = _inputs()
    rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    matches = tuple(find_inference_matches_for_rule(rule, definitions))
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == bridge


def test_pi5_3_goal_uses_exact_production_eta4_name():
    from dataclasses import replace

    from expression import Composition
    from homotopy_groups import FiniteCyclicGroup
    from proof import Relation

    _, goal, _ = _canonical_goals()
    generator = goal.rhs.generator
    assert isinstance(generator, Composition)
    assert generator.right.name == "η₄"
    assert generator.right.generator.index == 4

    wrong_generator = replace(
        generator, right=replace(generator.right, name="η_4")
    )
    wrong_goal = replace(
        goal, rhs=FiniteCyclicGroup(order=2, generator=wrong_generator)
    )
    assert wrong_goal != goal
    assert expand_phase162_pi5_3_group_goal(wrong_goal) is None
