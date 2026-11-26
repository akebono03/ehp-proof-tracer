"""Conditional tests only; hypothetical premises never enter a registry."""
from dataclasses import replace

import pytest

from expression import HomotopyElement
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap, TodaHopfInvariantMap,
    TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase178_r6_finite_group_cardinality_isolated.rule import expand_finite_cardinality_from_presentation
from phase178_r8_finite_group_surjective_injective_isolated.rule import (
    RULE_NAME, expand_finite_surjective_injective,
    finite_surjective_injective_inputs, valid_finite_group_map,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation,
    apply_inference_match, find_inference_matches_for_rule,
)


def delta(n=2, q=7):
    return TodaDeltaMap(TodaPrimaryGroup(q+2, 2*n+1), TodaPrimaryGroup(q, n))


def hypothetical(statement, trust=ProofRule.INFERENCE):
    return ProofStep(statement, (), trust, inference_rule=InferenceRule('test-only hypothesis'))


def replay(option, parents):
    matches = find_inference_matches_for_rule(option.rule, parents)
    step, = tuple(apply_inference_match(m) for m in matches
                  if all(a is b for a, b in zip(m.premises, parents))
                  and len(m.premises) == len(parents))
    assert step.rule is ProofRule.INFERENCE and step.premises == parents
    return step


@pytest.mark.parametrize('mapping,order', [
    (delta(), 2), (delta(4, 10), 8), (delta(6, 13), 16),
    (TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)), 4),
    (TodaHopfInvariantMap(TodaPrimaryGroup(10, 4), TodaPrimaryGroup(10, 7)), 8),
    (delta(3, 8), 1),
])
def test_generic_candidate_and_replay(mapping, order):
    goal = MapInjective(mapping)
    required = (FiniteGroupCardinality(mapping.source_group, order),
                FiniteGroupCardinality(mapping.target_group, order),
                MapSurjective(mapping))
    assert finite_surjective_injective_inputs(goal, order) == required
    option, = expand_finite_surjective_injective(goal, order)
    assert option.rule.name == RULE_NAME and option.subgoals == required
    assert replay(option, tuple(hypothetical(x) for x in required)).conclusion == goal


def test_different_group_structures_same_cardinality():
    # The conditional rule does not assume cyclic groups or equal generators.
    # Use two finite direct sums with different listed generators; the
    # surjectivity premise remains a test-only hypothesis.
    mapping = delta(4, 10)
    goal = MapInjective(mapping)
    option, = expand_finite_surjective_injective(goal, 8)
    parents = []
    for card, labels in zip(option.subgoals[:2], ('ab', 'cd')):
        group = card.group
        q, n = group.group_dimension, group.sphere_dimension
        presentation = Relation(group, DirectSumGroup(tuple(
            FiniteCyclicGroup(m, HomotopyElement(label, n, q, n))
            for m, label in zip((2, 4), labels)
        )))
        rule, = expand_finite_cardinality_from_presentation(card, presentation)
        parents.append(replay(rule, (hypothetical(presentation, ProofRule.GIVEN),)))
    parents.append(hypothetical(option.subgoals[2]))
    assert replay(option, tuple(parents)).conclusion == goal


def test_missing_or_untrusted_premises_rejected():
    option, = expand_finite_surjective_injective(MapInjective(delta()), 2)
    parents = tuple(hypothetical(x) for x in option.subgoals)
    for i in range(3):
        assert not find_inference_matches_for_rule(option.rule, parents[:i]+parents[i+1:])
        for trust in (ProofRule.GIVEN, ProofRule.RELATION):
            wrong = parents[:i]+(hypothetical(option.subgoals[i], trust),)+parents[i+1:]
            assert not find_inference_matches_for_rule(option.rule, wrong)
    assert not find_inference_matches_for_rule(option.rule, ())


def test_wrong_cardinality_group_or_map_rejected():
    mapping = delta()
    option, = expand_finite_surjective_injective(MapInjective(mapping), 2)
    a, b, surj = option.subgoals
    for bad in (replace(a, order=4), replace(a, order=2.0),
                replace(a, group=b.group)):
        assert not find_inference_matches_for_rule(option.rule, tuple(map(hypothetical, (bad,b,surj))))
    for bad in (replace(b, order=4), replace(b, order=2.0),
                replace(b, group=a.group)):
        assert not find_inference_matches_for_rule(option.rule, tuple(map(hypothetical, (a,bad,surj))))
    assert not find_inference_matches_for_rule(option.rule, tuple(map(hypothetical, (a,b,MapSurjective(delta(3,8))))))
    # Python bool compares equal to integer 1; exact runtime types still matter.
    unit, = expand_finite_surjective_injective(MapInjective(mapping), 1)
    a,b,surj = unit.subgoals
    assert not find_inference_matches_for_rule(unit.rule, tuple(map(hypothetical, (replace(a,order=True),b,surj))))


def test_invalid_typed_map_or_order_rejected():
    mapping = delta()
    for bad in (object(), replace(mapping,source_group=TodaPrimaryGroup(9,6)),
                replace(mapping,target_group=TodaPrimaryGroup(7,3)),
                TodaSuspensionMap(mapping.source_group,mapping.target_group),
                TodaHopfInvariantMap(mapping.source_group,mapping.target_group),
                TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,True))):
        assert not valid_finite_group_map(bad)
        assert not expand_finite_surjective_injective(MapInjective(bad), 2)
    for order in (True, False, 0, -2, 2.0, '2', None):
        assert not expand_finite_surjective_injective(MapInjective(mapping), order)
    assert not expand_finite_surjective_injective(MapSurjective(mapping), 2)
