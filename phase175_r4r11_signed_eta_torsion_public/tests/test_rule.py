"""Generic signed-to-exact normalization: strictly proved two-torsion and suspension."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import (
    Composition, GeneratorSymbol, HomotopyElement, MapApplication,
    Multiple, Sum, Zero,
)
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r11_signed_eta_torsion_public.rule import (
    RULE_NAME, eta_two_torsion_normalization_inputs,
    signed_eta_two_torsion_rule, expand_signed_eta_two_torsion,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture():
    source = canonical_toda58()
    beta = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", 7))
    gamma = HomotopyElement("η₉", 9, 10, 9, GeneratorSymbol("η", 9))
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(source.positive_value, beta),
    )
    order = Relation(Multiple(2, beta), Zero(), RelationType.EQUALITY)
    goal = Relation(
        MapApplication(EHP_DELTA_MAP, gamma),
        Composition(source.positive_value.right.expression, beta),
        RelationType.EQUALITY,
    )
    return goal, signed, order, TodaEtaFamilyGeneralDefinition()


def synthetic(value: object, kind: ProofRule) -> ProofStep:
    return ProofStep(value, (), kind, inference_rule=InferenceRule("test fixture"))


def test_canonical_delta_eta9_normalizes_without_direct_given() -> None:
    goal, signed, order, definition = fixture()
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition) == (
        signed, order, definition,
    )
    rule = signed_eta_two_torsion_rule(goal, signed, order, definition)
    assert rule.name == RULE_NAME
    parents = (
        synthetic(signed, ProofRule.INFERENCE),
        synthetic(order, ProofRule.INFERENCE),
        synthetic(definition, ProofRule.GIVEN),
    )
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == parents


def test_missing_sources_or_forged_given_not_accepted() -> None:
    goal, signed, order, definition = fixture()
    rule = signed_eta_two_torsion_rule(goal, signed, order, definition)
    parents = (
        synthetic(signed, ProofRule.INFERENCE),
        synthetic(order, ProofRule.INFERENCE),
        synthetic(definition, ProofRule.GIVEN),
    )
    for i in range(3):
        remaining = parents[:i] + parents[i + 1:]
        assert not find_inference_matches_for_rule(rule, remaining)
    assert not find_inference_matches_for_rule(rule, (
        synthetic(signed, ProofRule.GIVEN), parents[1], parents[2],
    ))
    assert not find_inference_matches_for_rule(rule, (
        parents[0], synthetic(order, ProofRule.GIVEN), parents[2],
    ))
    assert not find_inference_matches_for_rule(rule, (
        parents[0], parents[1], synthetic(definition, ProofRule.INFERENCE),
    ))


def test_general_even_coefficient_branch() -> None:
    goal, signed, order, definition = fixture()
    value = signed.positive_value
    changed = replace(value, left=replace(
        value.left, left=Multiple(8, value.left.left.expression),
    ))
    signed = replace(signed, positive_value=changed)
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition)


@pytest.mark.parametrize("coefficient", [1, 3, -3, True])
def test_odd_or_boolean_coefficient_rejected(coefficient: object) -> None:
    goal, signed, order, definition = fixture()
    value = signed.positive_value
    changed = replace(value, left=replace(
        value.left, left=Multiple(coefficient, value.left.left.expression),
    ))
    signed = replace(signed, positive_value=changed)
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition) is None


@pytest.mark.parametrize("change", [
    "wrong_order", "wrong_goal", "wrong_map", "wrong_beta", "wrong_sign", "not_suspension",
    "bad_definition", "changed_gamma", "invalid_type", "wrong_middle_group",
])
def test_unproved_or_malformed_rejected(change: str) -> None:
    goal, signed, order, definition = fixture()
    if change == "wrong_order":
        order = replace(order, lhs=Multiple(4, order.lhs.expression))
    elif change == "wrong_goal":
        goal = replace(goal, rhs=signed.positive_value)
    elif change == "wrong_map":
        goal = replace(goal, lhs=MapApplication(GeneratorSymbol("E"), signed.element))
    elif change == "wrong_beta":
        beta = replace(signed.positive_value.right, generator=GeneratorSymbol("ν", 7))
        signed = replace(signed, positive_value=replace(signed.positive_value, right=beta))
    elif change == "wrong_sign":
        linear = signed.positive_value.left
        signed = replace(signed, positive_value=replace(
            signed.positive_value,
            left=replace(linear, right=Multiple(1, linear.right.expression)),
        ))
    elif change == "not_suspension":
        beta = replace(signed.positive_value.right, dimension=2, source=3, target=2,
                       generator=GeneratorSymbol("η", 2))
        signed = replace(signed, positive_value=replace(signed.positive_value, right=beta))
    elif change == "bad_definition":
        definition = TodaEtaFamilyGeneralDefinition(lower_bound=4)
    elif change == "changed_gamma":
        signed = replace(signed, element=replace(signed.element, source=12))
    elif change == "invalid_type":
        signed = "signed Delta image text"
    elif change == "wrong_middle_group":
        signed = replace(signed, map=replace(signed.map,
                        target_group=TodaPrimaryGroup(9, 4)))
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition) is None


def test_source_discovered_expansion_not_a_proof_leaf() -> None:
    goal, signed, order, definition = fixture()
    options = expand_signed_eta_two_torsion(goal, (signed, signed))
    assert len(options) == 1
    assert options[0].subgoals == (signed, order, definition)
    assert not expand_signed_eta_two_torsion(goal, ())
    assert not expand_signed_eta_two_torsion(goal, ("source text",))
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)


def test_non_group_statement_does_not_claim_pi95() -> None:
    goal, signed, order, definition = fixture()
    assert isinstance(goal, Relation)
    assert goal.lhs.map == EHP_DELTA_MAP
    assert not hasattr(goal.lhs, "group_dimension")
    assert not hasattr(goal.rhs, "summands")
    with pytest.raises(ValueError):
        signed_eta_two_torsion_rule(goal, signed, replace(order, rhs=goal.rhs), definition)
