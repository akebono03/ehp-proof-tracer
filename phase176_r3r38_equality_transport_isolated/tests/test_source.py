"""R3R38 pure-rule tests; synthetic input steps are NOT proof certificates."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase176_r3r38_equality_transport_isolated.source import (
    replay_right_hopf_transport,
    right_hopf_transport_inputs,
)
from proof import ProofRule, ProofStep, Relation, RelationType


def _case():
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    delta = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    first = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    second = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    third = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    beta = Composition(first, second)
    gamma = Composition(second, third)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)),
                    Composition(delta, gamma), RelationType.EQUALITY)
    return alpha, delta, beta, gamma, goal


def _synthetic_inputs():
    _, _, beta, _, goal = _case()
    premises = right_hopf_transport_inputs(goal, beta)
    assert premises is not None
    return beta, goal, ProofStep(premises[0], (), ProofRule.INFERENCE), ProofStep(
        premises[1], (), ProofRule.INFERENCE,
    )


def test_builds_two_explicit_typed_obligations():
    alpha, delta, beta, gamma, goal = _case()
    substituted, suspension = right_hopf_transport_inputs(goal, beta)
    assert substituted.lhs.expression == Composition(alpha, Suspension(beta))
    assert substituted.rhs == Composition(delta, Suspension(beta))
    assert suspension == Relation(Suspension(beta), gamma, RelationType.EQUALITY)


def test_replays_six_preexisting_inference_rules_without_new_axioms():
    beta, goal, left, right = _synthetic_inputs()
    chain = replay_right_hopf_transport(goal, beta, left, right)
    assert len(chain) == 6
    assert chain[-1].conclusion == goal
    assert all(x.rule is ProofRule.INFERENCE for x in chain)
    assert [x.inference_rule.name for x in chain] == [
        "equality preserved under left composition",
        "EHP H preserves equality",
        "equality symmetry",
        "equality preserved under left composition",
        "equality transitivity",
        "equality transitivity",
    ]
    assert chain[0].premises == (right,)
    assert chain[3].premises == (right,)
    assert chain[4].premises == (chain[2], left)
    assert chain[5].premises == (chain[4], chain[3])


def test_independently_inferred_inputs_required():
    beta, goal, left, right = _synthetic_inputs()
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(goal, beta,
                                    ProofStep(left.conclusion, (), ProofRule.GIVEN), right)
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(goal, beta, left,
                                    ProofStep(right.conclusion, (), ProofRule.GIVEN))
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(goal, beta, None, right)


def test_wrong_suspension_or_formula_are_rejected():
    beta, goal, left, right = _synthetic_inputs()
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(
            goal, beta,
            ProofStep(replace(left.conclusion, rhs=goal.rhs), (), ProofRule.INFERENCE),
            right,
        )
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(
            goal, beta, left,
            ProofStep(replace(right.conclusion, rhs=beta), (), ProofRule.INFERENCE),
        )


def test_wrong_goal_shape_types_and_dimensions_fail_closed():
    alpha, delta, beta, gamma, goal = _case()
    assert right_hopf_transport_inputs(replace(goal, rhs=delta), beta) is None
    assert right_hopf_transport_inputs(replace(goal, rhs=Composition(delta, beta)), beta) is None
    assert right_hopf_transport_inputs(goal, delta) is None
    assert right_hopf_transport_inputs(replace(goal, lhs=goal.rhs), beta) is None
    assert right_hopf_transport_inputs(
        replace(goal, rhs=Composition(replace(delta, target=4), gamma)), beta,
    ) is None
    assert right_hopf_transport_inputs(
        replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(
            replace(alpha, source=100), gamma,
        ))), beta,
    ) is None
    with pytest.raises(ValueError, match="INVALID_TYPED_HOPF_TRANSPORT_GOAL"):
        replay_right_hopf_transport(replace(goal, rhs=delta), beta,
                                    ProofStep(goal, (), ProofRule.INFERENCE),
                                    ProofStep(goal, (), ProofRule.INFERENCE))


def test_not_hardcoded_to_nu_prime_eta_names():
    alpha, delta, beta, gamma, _ = _case()
    other_alpha = replace(alpha, name="formal-alpha", generator=None)
    other_delta = replace(delta, name="formal-delta", generator=None)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(other_alpha, gamma)),
                    Composition(other_delta, gamma), RelationType.EQUALITY)
    assert right_hopf_transport_inputs(goal, beta) is not None
    inputs = right_hopf_transport_inputs(goal, beta)
    assert inputs is not None
    steps = replay_right_hopf_transport(
        goal, beta,
        ProofStep(inputs[0], (), ProofRule.INFERENCE),
        ProofStep(inputs[1], (), ProofRule.INFERENCE),
    )
    assert steps[-1].conclusion == goal
