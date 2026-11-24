"""Focused R3R36 contracts. Synthetic ProofSteps are not source certificates."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula, expand_cited_prop22_right_formula,
)
from phase176_r3r36_composite_right_hopf_isolated.source import (
    COMPOSITE_FORMULA_RULE_NAME,
    COMPOSITE_SUBSTITUTION_RULE_NAME,
    composite_hopf_substitution_inputs,
    composite_hopf_substitution_rule,
    composite_right_formula_parts,
    expand_cited_composite_right_hopf,
)
from proof import (
    ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_match,
)


def elements():
    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    return nu_prime, eta5, eta6, eta7


def typed_goals():
    nu_prime, eta5, eta6, eta7 = elements()
    suspended_composite = Suspension(Composition(eta5, eta6))
    lhs = MapApplication(EHP_H_MAP, Composition(nu_prime, suspended_composite))
    formula = Relation(
        lhs, Composition(MapApplication(EHP_H_MAP, nu_prime), suspended_composite),
        RelationType.EQUALITY,
    )
    substituted = Relation(
        lhs, Composition(eta5, suspended_composite), RelationType.EQUALITY,
    )
    hopf = Relation(MapApplication(EHP_H_MAP, nu_prime), eta5, RelationType.EQUALITY)
    return formula, substituted, hopf


def test_composite_formula_is_cited_and_keeps_its_right_factor():
    formula, substituted, hopf = typed_goals()
    nu_prime, eta5, eta6, eta7 = elements()
    assert composite_right_formula_parts(formula) == (nu_prime, Composition(eta5, eta6))
    assert expand_cited_composite_right_hopf(formula, ()) == ()
    assert expand_cited_composite_right_hopf(
        formula, (TodaProp22RightFormula(), TodaProp22RightFormula()),
    ) == ()
    choices = expand_cited_composite_right_hopf(formula, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].rule.name == COMPOSITE_FORMULA_RULE_NAME
    assert choices[0].subgoals == (TodaProp22RightFormula(),)


def test_composite_substitution_has_two_independent_proof_goals():
    formula, substituted, hopf = typed_goals()
    assert composite_hopf_substitution_inputs(substituted) == (formula, hopf)
    choices = expand_cited_composite_right_hopf(substituted, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].rule.name == COMPOSITE_SUBSTITUTION_RULE_NAME
    assert choices[0].subgoals == (formula, hopf)
    assert expand_cited_composite_right_hopf(substituted, ()) == ()


def test_inference_replay_requires_proved_formula_and_hopf_value():
    formula, substituted, hopf = typed_goals()
    formal_rule = expand_cited_composite_right_hopf(
        formula, (TodaProp22RightFormula(),),
    )[0].rule
    simulated_source = ProofStep(TodaProp22RightFormula(), (), ProofRule.GIVEN)
    formal_match = find_inference_match(formal_rule, (simulated_source,))
    assert formal_match is not None
    formal_step = apply_inference_match(formal_match)
    assert formal_step.conclusion == formula
    assert formal_step.rule is ProofRule.INFERENCE
    substitute_rule = composite_hopf_substitution_rule(substituted)
    simulated_hopf = ProofStep(hopf, (), ProofRule.GIVEN)
    match = find_inference_match(substitute_rule, (formal_step, simulated_hopf))
    assert match is not None
    result = apply_inference_match(match)
    assert result.conclusion == substituted
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (formal_step, simulated_hopf)
    assert find_inference_match(
        substitute_rule,
        (ProofStep(formula, (), ProofRule.GIVEN), simulated_hopf),
    ) is None
    assert find_inference_match(
        substitute_rule,
        (formal_step, ProofStep(replace(hopf, rhs=elements()[2]), (), ProofRule.GIVEN)),
    ) is None


def test_composite_right_wrong_types_and_rhs_fail_closed():
    formula, substituted, hopf = typed_goals()
    nu_prime, eta5, eta6, eta7 = elements()
    wrong_alpha = replace(nu_prime, source=30)
    malformed = Relation(
        MapApplication(EHP_H_MAP, Composition(
            wrong_alpha, Suspension(Composition(eta5, eta6)),
        )),
        Composition(MapApplication(EHP_H_MAP, wrong_alpha),
                    Suspension(Composition(eta5, eta6))),
        RelationType.EQUALITY,
    )
    assert composite_right_formula_parts(malformed) is None
    wrong_rhs = replace(formula, rhs=Composition(eta5, formula.rhs.right))
    assert composite_right_formula_parts(wrong_rhs) is None
    bad_hopf_value = replace(substituted, rhs=Composition(eta6, substituted.rhs.right))
    assert composite_hopf_substitution_inputs(bad_hopf_value) is None
    wrong_suspended_right = replace(substituted, rhs=Composition(eta5, Suspension(Composition(eta6, eta7))))
    assert composite_hopf_substitution_inputs(wrong_suspended_right) is None
    assert expand_cited_composite_right_hopf(bad_hopf_value, (TodaProp22RightFormula(),)) == ()
    with pytest.raises(ValueError):
        composite_hopf_substitution_rule(bad_hopf_value)


def test_old_single_right_factor_remains_old_provider_responsibility():
    nu_prime, eta5, eta6, eta7 = elements()
    formula = Relation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, Suspension(eta5))),
        Composition(MapApplication(EHP_H_MAP, nu_prime), Suspension(eta5)),
        RelationType.EQUALITY,
    )
    assert expand_cited_composite_right_hopf(formula, (TodaProp22RightFormula(),)) == ()
    assert len(expand_cited_prop22_right_formula(formula, (TodaProp22RightFormula(),))) == 1


def test_general_composite_left_and_composite_right_are_well_typed():
    nu_prime, eta5, eta6, eta7 = elements()
    alpha = Composition(nu_prime, eta6)
    beta = Composition(eta6, eta7)
    right = Suspension(beta)
    delta = HomotopyElement("δ", 5, 7, 5)
    substituted = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, right)),
        Composition(delta, right), RelationType.EQUALITY,
    )
    inputs = composite_hopf_substitution_inputs(substituted)
    assert inputs is not None
    assert inputs[1] == Relation(MapApplication(EHP_H_MAP, alpha), delta,
                                 RelationType.EQUALITY)


def test_provider_rejects_non_tuple_available():
    formula, substituted, hopf = typed_goals()
    with pytest.raises(TypeError):
        expand_cited_composite_right_hopf(formula, [TodaProp22RightFormula()])
