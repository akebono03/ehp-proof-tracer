"""Focused contracts for typed eta notation obligations, not proof fixtures."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r27r1_toda55_quadruple_isolated.source import Toda55UniversalQuadrupleStatement, canonical_quadruple_goal
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan, eta_notation_backward_plan
from proof import ProofRule, ProofStep, Relation, apply_inference_match, find_inference_match
from toda_rules import toda_eta_family_definition_statement


def unicode_eta(n):
    canonical = toda_eta_family_definition_statement(n).element
    name = "η" + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return replace(canonical, name=name)


def example():
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    e5, e6, e7 = (unicode_eta(n) for n in (5, 6, 7))
    gamma = Composition(e6, e7)
    forward = canonical_quadruple_goal(5)
    transport = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)), Composition(e5, gamma))
    available = (TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula(),
                 Toda55UniversalQuadrupleStatement(), CitedStableFamilyDefinition(4, 4, 3),
                 Relation(MapApplication(EHP_H_MAP, alpha), e5))
    return transport, forward, available


def test_real_canonical_spelling_differs_but_has_same_typed_symbol():
    observed = unicode_eta(5)
    canonical = toda_eta_family_definition_statement(5).element
    assert observed.name == "η₅" and canonical.name == "η_5"
    assert observed != canonical
    assert replace(observed, name=canonical.name) == canonical


@pytest.mark.parametrize("n", (5, 6, 7))
def test_leaf_requires_two_suspension_equalities_and_old_rules(n):
    a, b = unicode_eta(n), toda_eta_family_definition_statement(n).element
    plan = eta_notation_backward_plan(a, b, (TodaEtaFamilyGeneralDefinition(),))
    assert len(plan) == 4
    assert plan[-1][0] == Relation(a, b)
    assert [x.rule.name for _, x in plan] == [
        "proved consecutive eta suspension yields element equality",
        "proved consecutive eta suspension yields element equality",
        "equality symmetry", "equality transitivity",
    ]
    witness, = plan[0][1].subgoals
    assert isinstance(witness, GeneratorSuspension)
    assert plan[1][1].subgoals == (witness,)
    assert plan[0][0].lhs == Suspension(witness.source_generator)


def test_cube_plan_replays_existing_rules_with_synthetic_witnesses_only():
    transport, forward, available = example()
    plan = eta_notation_backward_plan(transport.rhs, forward.rhs, available)
    assert len(plan) == 18
    steps = {}
    for target, option in plan:
        for child in option.subgoals:
            if isinstance(child, GeneratorSuspension):
                # Synthetic witness is a unit-test fixture, never a production proof.
                steps.setdefault(child, ProofStep(child, (), ProofRule.INFERENCE))
        premises = tuple(steps[child] for child in option.subgoals)
        match = find_inference_match(option.rule, premises)
        assert match is not None
        result = apply_inference_match(match)
        assert result.conclusion == target and result.rule is ProofRule.INFERENCE
        assert result.premises == premises
        steps[target] = result
    assert Relation(transport.rhs, forward.rhs) in steps


def test_sources_and_type_checks_refuse_forgery():
    a, b = unicode_eta(5), toda_eta_family_definition_statement(5).element
    source = TodaEtaFamilyGeneralDefinition()
    assert eta_notation_backward_plan(a, b, ()) == ()
    assert eta_notation_backward_plan(a, b, (source, source)) == ()
    assert eta_notation_backward_plan(a, a, (source,)) == ()
    for forged in (replace(b, name="eta_5"), replace(b, source=99),
                   replace(b, generator=GeneratorSymbol("ν", index=5))):
        assert eta_notation_backward_plan(a, forged, (source,)) == ()
    with pytest.raises(TypeError):
        eta_notation_backward_plan(a, b, [source])


def test_connection_keeps_independent_obligations_and_final_old_rules():
    transport, forward, available = example()
    plan = connection_backward_plan(transport, forward, available)
    assert len(plan) == 21
    alias = Relation(transport.rhs, forward.rhs)
    aligned = Relation(transport.lhs, forward.rhs)
    reverse = Relation(forward.rhs, forward.lhs)
    final = Relation(transport.lhs, forward.lhs)
    assert plan[-3][0] == aligned and plan[-3][1].subgoals == (transport, alias)
    assert plan[-2][0] == reverse and plan[-2][1].subgoals == (forward,)
    assert plan[-1][0] == final and plan[-1][1].subgoals == (aligned, reverse)
    assert transport not in dict(plan) and forward not in dict(plan)
    for i in range(len(available)):
        assert connection_backward_plan(transport, forward, available[:i] + available[i+1:]) == ()


def test_notation_does_not_reassociate_composition():
    transport, forward, available = example()
    cube = forward.rhs
    reassociated = Composition(Composition(cube.left, cube.right.left), cube.right.right)
    assert eta_notation_backward_plan(transport.rhs, reassociated, available) == ()
