"""Focused isolated rule contracts, including reuse of actual cited sources."""
from __future__ import annotations

from dataclasses import replace
import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25, build_cited_58_prop25_sources
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511, build_cited_511_source
from phase175_r4r12r10r1_cited_511_public.provider import expand_cited_511
from phase177_r3_unsigned_delta_composition_isolated.rule import (
    RULE_NAME, unsigned_prop25_inputs, unsigned_prop25_rule, expand_unsigned_prop25,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def element(name, source, target):
    return HomotopyElement(name, target, source=source, target=target)


def fixture(m=4, i=9, j=10):
    alpha = element('a', i+1, 2*m+1)
    beta = element('b', j-1, i-1)
    x = element('x', i-1, m)
    gamma = element('g', j+1, 2*m+1)
    explicit = Composition(alpha, IteratedSuspension(beta, 2))
    base = Relation(MapApplication(EHP_DELTA_MAP, alpha), x)
    identity = Relation(explicit, gamma)
    goal = Relation(MapApplication(EHP_DELTA_MAP, gamma), Composition(x, beta))
    return goal, base, identity


def synthetic(statement, trust=ProofRule.INFERENCE):
    return ProofStep(statement, (), trust, inference_rule=InferenceRule('synthetic test parent'))


def test_literal_formula_needs_no_reflexive_premise():
    goal, base, identity = fixture()
    literal = replace(goal, lhs=MapApplication(EHP_DELTA_MAP, identity.lhs))
    expansion, = expand_unsigned_prop25(literal, base)
    assert expansion.subgoals == (CitedTodaProp25(), base)
    assert expansion.rule.name == RULE_NAME
    assert not expand_unsigned_prop25(goal, base)


def test_substitution_requires_independent_composition_identity():
    goal, base, identity = fixture()
    expansion, = expand_unsigned_prop25(goal, base, identity)
    assert expansion.subgoals == (CitedTodaProp25(), base, identity)
    parents = (synthetic(CitedTodaProp25(), ProofRule.GIVEN), synthetic(base), synthetic(identity))
    matches = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(matches) == 1
    result = apply_inference_match(matches[0])
    assert result.conclusion == goal and result.rule is ProofRule.INFERENCE
    assert result.premises == parents


@pytest.mark.parametrize('m,i,j', [(3,6,10),(4,9,10),(5,11,15)])
def test_valid_general_dimensions(m,i,j):
    assert unsigned_prop25_inputs(*fixture(m,i,j)) is not None


@pytest.mark.parametrize('m,i,j', [(4,9,11),(4,9,12),(6,12,17),(1,2,3),(4,7,9),(4,9,8)])
def test_outside_verified_range(m,i,j):
    assert not expand_unsigned_prop25(*fixture(m,i,j))


@pytest.mark.parametrize('change', ['map','base_map','wrong_x','wrong_beta','wrong_gamma','exponent','reverse','not_equality'])
def test_rejects_mismatched_typed_input(change):
    goal, base, identity = fixture()
    if change == 'map':
        goal = replace(goal, lhs=MapApplication(EHP_H_MAP, goal.lhs.expression))
    elif change == 'base_map':
        base = replace(base, lhs=MapApplication(EHP_H_MAP, base.lhs.expression))
    elif change == 'wrong_x':
        goal = replace(goal, rhs=Composition(element('different',8,4),goal.rhs.right))
    elif change == 'wrong_beta':
        goal = replace(goal, rhs=Composition(base.rhs,element('different',9,8)))
    elif change == 'wrong_gamma':
        identity = replace(identity, rhs=element('different',11,9))
    elif change == 'exponent':
        identity = replace(identity, lhs=Composition(identity.lhs.left,IteratedSuspension(goal.rhs.right,1)))
    elif change == 'reverse':
        identity = replace(identity, lhs=identity.rhs, rhs=identity.lhs)
    else:
        base = replace(base, relation_type=RelationType.ORDER)
    assert not expand_unsigned_prop25(goal, base, identity)


@pytest.mark.parametrize('missing', [0,1,2])
def test_missing_parent_rejected(missing):
    goal, base, identity = fixture()
    rule = unsigned_prop25_rule(goal, base, identity)
    parents = (synthetic(CitedTodaProp25(),ProofRule.GIVEN),synthetic(base),synthetic(identity))
    assert not find_inference_matches_for_rule(rule, parents[:missing]+parents[missing+1:])


@pytest.mark.parametrize('changed', [0,1,2])
def test_wrong_trust_rejected(changed):
    goal, base, identity = fixture()
    rule = unsigned_prop25_rule(goal, base, identity)
    parents = [synthetic(CitedTodaProp25(),ProofRule.GIVEN),synthetic(base),synthetic(identity)]
    parents[changed] = synthetic(parents[changed].conclusion,
                                 ProofRule.INFERENCE if changed == 0 else ProofRule.GIVEN)
    assert not find_inference_matches_for_rule(rule, tuple(parents))


def test_wrong_citation_and_circular_goal_rejected():
    goal, base, identity = fixture()
    rule = unsigned_prop25_rule(goal, base, identity)
    parents = (synthetic(CitedTodaProp25('other'),ProofRule.GIVEN),synthetic(base),synthetic(identity))
    assert not find_inference_matches_for_rule(rule, parents)
    assert not expand_unsigned_prop25(base, base)


def test_actual_511_and_prop25_sources_derive_literal_formula():
    base = canonical_511()
    citation = CitedToda511(base)
    source511 = build_cited_511_source()
    source25 = build_cited_58_prop25_sources()
    step511, = [link.step for link in source511.proof_links if link.step.conclusion == citation]
    step25, = [link.step for link in source25.proof_links if link.step.conclusion == CitedTodaProp25()]
    expansion, = expand_cited_511(base, (citation,))
    match, = find_inference_matches_for_rule(expansion.rule, (step511,))
    base_step = apply_inference_match(match)
    beta = HomotopyElement('η₈',8,9,8,GeneratorSymbol('η',index=8))
    goal = Relation(MapApplication(EHP_DELTA_MAP, Composition(base.lhs.expression,IteratedSuspension(beta,2))),
                    Composition(base.rhs,beta))
    option, = expand_unsigned_prop25(goal, base)
    match, = find_inference_matches_for_rule(option.rule,(step25,base_step))
    result = apply_inference_match(match)
    assert result.conclusion == goal and result.rule is ProofRule.INFERENCE
    assert result.premises == (step25,base_step)
    assert base_step.premises == (step511,)
