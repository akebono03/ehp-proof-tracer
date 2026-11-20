"""R3R30 focused contracts: independent proof obligations, no forged facts."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r30_generic_hopf_substitution_isolated.source import (
    expand_generic_hopf_substitution, generic_hopf_substitution_inputs,
    generic_hopf_substitution_rule,
)
from proof import (
    ProofRule, ProofStep, Relation, RelationType,
    find_inference_matches_for_rule, apply_inference_match,
)


def elements():
    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    return nu, eta5, eta6


def goal_and_inputs():
    nu, eta5, eta6 = elements()
    alpha = Composition(nu, eta6)
    right = Suspension(eta6)
    delta = Composition(eta5, eta6)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, right)),
        Composition(delta, right),
        RelationType.EQUALITY,
    )
    inputs = generic_hopf_substitution_inputs(goal)
    assert inputs is not None
    return goal, inputs


def test_two_independent_subgoals_for_composite_left() -> None:
    goal, inputs = goal_and_inputs()
    choices = expand_generic_hopf_substitution(goal, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].subgoals == inputs
    assert inputs[0].lhs == goal.lhs
    assert inputs[1].lhs.expression == goal.lhs.expression.left


def test_proved_formula_and_hopf_value_close_by_inference() -> None:
    goal, (formula, hopf_value) = goal_and_inputs()
    rule = generic_hopf_substitution_rule(goal)
    premises = (ProofStep(formula, (), ProofRule.INFERENCE),
                ProofStep(hopf_value, (), ProofRule.INFERENCE))
    matches = find_inference_matches_for_rule(rule, premises)
    assert len(matches) == 1
    result = apply_inference_match(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == premises


def test_wrong_hopf_value_or_unproved_formula_rejected() -> None:
    goal, (formula, hopf_value) = goal_and_inputs()
    rule = generic_hopf_substitution_rule(goal)
    cited = ProofStep(formula, (), ProofRule.INFERENCE)
    wrong = ProofStep(replace(hopf_value, rhs=elements()[1]), (), ProofRule.INFERENCE)
    assert not find_inference_matches_for_rule(rule, (cited, wrong))
    direct_formula = ProofStep(formula, (), ProofRule.GIVEN)
    genuine_hopf = ProofStep(hopf_value, (), ProofRule.INFERENCE)
    assert not find_inference_matches_for_rule(rule, (direct_formula, genuine_hopf))


def test_cited_general_formula_required() -> None:
    goal, _ = goal_and_inputs()
    assert expand_generic_hopf_substitution(goal, ()) == ()
    assert expand_generic_hopf_substitution(
        goal, (TodaProp22RightFormula(), TodaProp22RightFormula()),
    ) == ()


def test_type_and_rhs_fail_closed() -> None:
    goal, _ = goal_and_inputs()
    assert generic_hopf_substitution_inputs(replace(goal, rhs=goal.rhs.left)) is None
    assert generic_hopf_substitution_inputs(
        replace(goal, rhs=Composition(goal.rhs.left, elements()[1]))
    ) is None
    with pytest.raises(ValueError):
        generic_hopf_substitution_rule(replace(goal, rhs=goal.rhs.left))
