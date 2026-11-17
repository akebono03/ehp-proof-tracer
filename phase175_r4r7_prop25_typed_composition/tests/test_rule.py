"""Synthetic-only typed inference tests. No Toda proof is registered here."""
from __future__ import annotations

from dataclasses import replace
import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, ScalarSymbol, Sum
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from toda_rules import TodaDeltaImageUpToSignStatement
from phase175_r4r7_prop25_typed_composition.rule import (
    RULE_NAME, typed_endpoints, prop25_inputs, prop25_signed_composition_rule,
    expand_prop25_signed_composition,
)


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(name, target, source=source, target=target)


def fixture(m: int = 4, i: int = 8, j: int = 9):
    alpha = element('iota', i + 1, 2 * m + 1)
    beta = element('beta', j - 1, i - 1)
    gamma = element('gamma', j + 1, 2 * m + 1)
    positive = Sum(Multiple(2, element('x', i - 1, m)),
                   Multiple(-1, element('y', i - 1, m)))
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(i + 1, 2 * m + 1), TodaPrimaryGroup(i - 1, m)),
        alpha, positive,
    )
    identity = Relation(Composition(alpha, IteratedSuspension(beta, 2)),
                        gamma, RelationType.EQUALITY)
    goal = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(j + 1, 2 * m + 1), TodaPrimaryGroup(j - 1, m)),
        gamma, Composition(positive, beta),
    )
    return goal, signed, identity


def synthetic(conclusion, rule: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(conclusion, (), rule, inference_rule=InferenceRule('synthetic fixture'))


def test_m4_i8_j9_typed() -> None:
    goal, signed, identity = fixture()
    assert prop25_inputs(goal, signed, identity) == (signed, identity)
    assert typed_endpoints(signed.element) == (9, 9)
    assert typed_endpoints(identity.lhs.right) == (10, 9)
    assert typed_endpoints(goal.positive_value) == (8, 4)


def test_two_independent_verified_steps_produce_signed_proofstep() -> None:
    goal, signed, identity = fixture()
    rule = prop25_signed_composition_rule(goal, signed, identity)
    assert rule.name == RULE_NAME
    parents = (synthetic(signed), synthetic(identity))
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == parents


def test_sign_not_canceled_and_only_signed_conclusion() -> None:
    goal, signed, identity = fixture()
    assert goal.positive_value == Composition(signed.positive_value, identity.lhs.right.expression)
    assert goal.positive_value.left.right.coefficient == -1
    assert isinstance(goal, TodaDeltaImageUpToSignStatement)
    assert not isinstance(goal, Relation)


def test_expansion_does_not_create_proof_or_given() -> None:
    goal, signed, identity = fixture()
    expansions = expand_prop25_signed_composition(goal, signed, identity)
    assert len(expansions) == 1
    assert expansions[0].subgoals == (signed, identity)
    assert all(not isinstance(statement, ProofStep) for statement in expansions[0].subgoals)
    assert goal not in expansions[0].subgoals
    assert not find_inference_matches_for_rule(expansions[0].rule, ())


@pytest.mark.parametrize('missing', (0, 1))
def test_missing_premise_rejects(missing: int) -> None:
    goal, signed, identity = fixture()
    parents = (synthetic(signed), synthetic(identity))
    assert not find_inference_matches_for_rule(
        prop25_signed_composition_rule(goal, signed, identity),
        parents[:missing] + parents[missing + 1:],
    )


@pytest.mark.parametrize('changed', (0, 1))
def test_forged_given_rejects(changed: int) -> None:
    goal, signed, identity = fixture()
    parents = [synthetic(signed), synthetic(identity)]
    parents[changed] = synthetic(parents[changed].conclusion, ProofRule.GIVEN)
    assert not find_inference_matches_for_rule(
        prop25_signed_composition_rule(goal, signed, identity), tuple(parents),
    )


def test_general_odd_m_branch() -> None:
    goal, signed, identity = fixture(3, 6, 10)
    assert 10 >= 3 * 3 - 1
    assert prop25_inputs(goal, signed, identity) == (signed, identity)


def test_general_even_m_bounded_branch() -> None:
    goal, signed, identity = fixture(4, 8, 10)
    assert prop25_inputs(goal, signed, identity) == (signed, identity)


@pytest.mark.parametrize('m,i,j', ((4, 8, 11), (4, 8, 12), (6, 12, 17)))
def test_even_m_unproved_two_primary_branch_rejected(m: int, i: int, j: int) -> None:
    goal, signed, identity = fixture(m, i, j)
    assert prop25_inputs(goal, signed, identity) is None
    assert not expand_prop25_signed_composition(goal, signed, identity)


@pytest.mark.parametrize('m,i,j', ((1, 2, 3), (4, 7, 9), (4, 8, 7)))
def test_invalid_dimensions_rejected(m: int, i: int, j: int) -> None:
    assert prop25_inputs(*fixture(m, i, j)) is None


@pytest.mark.parametrize('change', ('signed_map', 'goal_map', 'gamma', 'order', 'exponent', 'unsigned', 'relation'))
def test_malformed_statement_rejected(change: str) -> None:
    goal, signed, identity = fixture()
    if change == 'signed_map':
        signed = replace(signed, map=goal.map)
    elif change == 'goal_map':
        goal = replace(goal, map=signed.map)
    elif change == 'gamma':
        identity = replace(identity, rhs=element('wrong', 10, 9))
    elif change == 'order':
        identity = replace(identity, lhs=Composition(identity.lhs.right, identity.lhs.left))
    elif change == 'exponent':
        identity = replace(identity, lhs=Composition(identity.lhs.left, IteratedSuspension(identity.lhs.right.expression, 1)))
    elif change == 'unsigned':
        goal = replace(goal, positive_value=Composition(signed.positive_value.right.expression, identity.lhs.right.expression))
    else:
        identity = replace(identity, relation_type=RelationType.ORDER)
    assert prop25_inputs(goal, signed, identity) is None


@pytest.mark.parametrize('invalid', (
    element('bad', 6, 8), element('bad', 1, 1),
    HomotopyElement('bad', 9, source=True, target=9),
    IteratedSuspension(element('x', 7, 4), -1),
    IteratedSuspension(element('x', 7, 4), ScalarSymbol('n')),
    Multiple(ScalarSymbol('k'), element('x', 7, 4)),
    Sum(element('x', 7, 4), element('y', 7, 5)),
))
def test_untyped_expression_rejected(invalid: object) -> None:
    assert typed_endpoints(invalid) is None


def test_general_integer_linear_composition_endpoints() -> None:
    x, y, beta = element('x', 8, 5), element('y', 8, 5), element('b', 10, 8)
    assert typed_endpoints(Sum(Multiple(3, x), Multiple(-2, y))) == (8, 5)
    assert typed_endpoints(Composition(x, beta)) == (10, 5)


def test_printed_text_is_not_a_typed_goal_or_premise() -> None:
    goal, signed, identity = fixture()
    assert prop25_inputs('Delta eta9', signed, identity) is None
    assert prop25_inputs(goal, 'source formula', identity) is None
    assert prop25_inputs(goal, signed, 'source formula') is None
    with pytest.raises(ValueError, match='not a typed'):
        prop25_signed_composition_rule(goal, signed, 'source formula')
