"""Synthetic premises only: no registered GIVEN or public proof is created."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase178_r6_finite_group_cardinality_isolated.rule import (
    RULE_NAME, cardinality_from_presentation, expand_finite_cardinality_from_presentation,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def presentation(n, k, orders):
    group = TodaPrimaryGroup(n+k, n)
    parts = tuple(FiniteCyclicGroup(m, HomotopyElement(f'g{j}', n, n+k, n))
                  for j, m in enumerate(orders))
    return Relation(group, parts[0] if len(parts) == 1 else DirectSumGroup(parts))


@pytest.mark.parametrize('n,k,orders,total', [
    (2,5,(2,),2), (5,4,(2,),2), (4,6,(8,),8), (7,3,(16,),16),
    (4,5,(2,2),4), (6,9,(2,4,8),64),
])
def test_cardinality_and_replay(n,k,orders,total):
    claim = presentation(n,k,orders)
    goal = FiniteGroupCardinality(claim.lhs,total)
    assert cardinality_from_presentation(claim) == goal
    option, = expand_finite_cardinality_from_presentation(goal,claim)
    assert option.rule.name == RULE_NAME and option.subgoals == (claim,)
    for trust in (ProofRule.GIVEN, ProofRule.INFERENCE):
        parent = ProofStep(claim, (), trust, inference_rule=InferenceRule('test-only hypothesis'))
        match, = find_inference_matches_for_rule(option.rule,(parent,))
        step = apply_inference_match(match)
        assert step.rule is ProofRule.INFERENCE
        assert step.conclusion == goal and step.premises == (parent,)
    assert not find_inference_matches_for_rule(option.rule,())


def test_composite_generator_is_accepted():
    claim = presentation(2,5,(2,))
    g = Composition(HomotopyElement('a',2,3,2), HomotopyElement('b',3,7,3))
    claim = replace(claim,rhs=FiniteCyclicGroup(2,g))
    assert cardinality_from_presentation(claim) == FiniteGroupCardinality(claim.lhs,2)


def test_reject_infinite_or_malformed_presentations():
    claim = presentation(4,5,(2,4))
    a,b = claim.rhs.summands
    for structure in (FreeCyclicGroup(a.generator), DirectSumGroup((a,FreeCyclicGroup(b.generator))),
                      DirectSumGroup(()), DirectSumGroup((a,)), DirectSumGroup([a,b]),
                      DirectSumGroup((a,a)), DirectSumGroup((a,object())),
                      FiniteCyclicGroup(True,a.generator), FiniteCyclicGroup(0,a.generator),
                      FiniteCyclicGroup(1,a.generator), FiniteCyclicGroup(-2,a.generator),
                      FiniteCyclicGroup(2,replace(a.generator,source=10))):
        assert cardinality_from_presentation(replace(claim,rhs=structure)) is None
    assert cardinality_from_presentation(replace(claim,relation_type=RelationType.ORDER)) is None
    assert cardinality_from_presentation(replace(claim,lhs=TodaPrimaryGroup(True,4))) is None
    assert cardinality_from_presentation(TodaPrimaryGroupZeroStatement(claim.lhs)) is None


def test_reject_wrong_goal_or_unproved_premise():
    claim = presentation(4,5,(2,4))
    goal = FiniteGroupCardinality(claim.lhs,8)
    for bad in (replace(goal,order=4), replace(goal,order=True), replace(goal,order=8.0),
                replace(goal,group=TodaPrimaryGroup(10,4)), object()):
        assert not expand_finite_cardinality_from_presentation(bad,claim)
    option, = expand_finite_cardinality_from_presentation(goal,claim)
    assert not find_inference_matches_for_rule(option.rule,(ProofStep(claim,(),ProofRule.RELATION),))
    wrong = presentation(4,5,(2,2))
    assert not find_inference_matches_for_rule(option.rule,(ProofStep(wrong,(),ProofRule.GIVEN),))
