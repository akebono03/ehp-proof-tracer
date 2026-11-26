"""Test-only conditional hypotheses; no registered GIVEN or public hook."""
from dataclasses import replace

import pytest

from expression import HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import (
    ORDER_RULE, INJECTIVE_RULE, expand_summand_generator_order, expand_finite_delta_injective,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule


def fixture(n=4, m=2):
    source = TodaPrimaryGroup(2*n+2, 2*n+1)
    target = TodaPrimaryGroup(2*n, n)
    a = HomotopyElement('a', 2*n+1, 2*n+2, 2*n+1)
    b = HomotopyElement('b', n, 2*n, n)
    c = HomotopyElement('c', n, 2*n, n)
    delta = TodaDeltaMap(source, target)
    domain = Relation(source, FiniteCyclicGroup(m, a))
    codomain = Relation(target, DirectSumGroup((FiniteCyclicGroup(m, b), FiniteCyclicGroup(2, c))))
    return MapInjective(delta), domain, codomain, GeneratorImage(delta, a, b), FiniteElementOrder(target, b, m)


def hypothetical(statement, trust=ProofRule.INFERENCE):
    return ProofStep(statement, (), trust, inference_rule=InferenceRule('test-only hypothesis'))


def replay(option, parents, conclusion):
    matches = find_inference_matches_for_rule(option.rule, parents)
    step, = tuple(apply_inference_match(m) for m in matches if m.premises == parents)
    assert step.conclusion == conclusion and step.rule is ProofRule.INFERENCE
    assert step.premises == parents
    return step


@pytest.mark.parametrize('n,m', [(3,2),(4,2),(5,4),(6,8),(7,16)])
def test_conditional_chain(n, m):
    goal, domain, codomain, image, order = fixture(n,m)
    first, = expand_summand_generator_order(order, codomain)
    second, = expand_finite_delta_injective(goal, domain, image, order)
    assert first.rule.name == ORDER_RULE and first.subgoals == (codomain,)
    assert second.rule.name == INJECTIVE_RULE and second.subgoals == (domain,image,order)
    o = replay(first, (hypothetical(codomain, ProofRule.GIVEN),), order)
    replay(second, (hypothetical(domain, ProofRule.GIVEN), hypothetical(image), o), goal)
    assert not find_inference_matches_for_rule(first.rule, ())
    assert not find_inference_matches_for_rule(second.rule, ())


def test_order_supports_mixed_and_many_summands():
    _, _, codomain, _, order = fixture(5,8)
    b,c = codomain.rhs.summands
    d = HomotopyElement('d',5,10,5)
    for parts in ((FreeCyclicGroup(c.generator),b),(b,c,FiniteCyclicGroup(4,d))):
        claim = replace(codomain,rhs=DirectSumGroup(parts))
        assert expand_summand_generator_order(order,claim)


def test_reject_wrong_order_and_presentation():
    _, _, codomain, _, order = fixture()
    b,c = codomain.rhs.summands
    wrong = HomotopyElement('unknown',4,8,4)
    for bad in (replace(order,order=4),replace(order,order=True),replace(order,element=wrong),
                replace(order,group=TodaPrimaryGroup(9,4))):
        assert not expand_summand_generator_order(bad,codomain)
    for bad in (replace(codomain,relation_type=RelationType.ORDER),
                replace(codomain,rhs=DirectSumGroup((b,b))),
                replace(codomain,rhs=DirectSumGroup((FreeCyclicGroup(b.generator),c))),
                replace(codomain,rhs=DirectSumGroup((b,FiniteCyclicGroup(0,c.generator)))),
                replace(codomain,rhs=DirectSumGroup((b,FiniteCyclicGroup(2,replace(c.generator,source=9))))),
                replace(codomain,rhs=b)):
        assert not expand_summand_generator_order(order,bad)


def test_reject_wrong_delta_and_generator_order():
    goal, domain, _, image, order = fixture(4,4)
    other = HomotopyElement('other',9,10,9)
    for bad in (replace(domain,rhs=FiniteCyclicGroup(2,domain.rhs.generator)),
                replace(domain,rhs=FiniteCyclicGroup(4,other)),
                replace(domain,relation_type=RelationType.ORDER),
                replace(domain,rhs=FreeCyclicGroup(domain.rhs.generator))):
        assert not expand_finite_delta_injective(goal,bad,image,order)
    for bad in (replace(order,order=2),replace(order,order=True),
                replace(order,element=replace(order.element,name='other')),
                replace(order,group=TodaPrimaryGroup(9,4))):
        assert not expand_finite_delta_injective(goal,domain,image,bad)
    for bad in (replace(image,source_generator=other),
                replace(image,target_generator=replace(image.target_generator,source=9)),
                replace(image,map=TodaDeltaMap(TodaPrimaryGroup(11,9),goal.map.target_group))):
        assert not expand_finite_delta_injective(goal,domain,bad,order)
    invalid = TodaDeltaMap(goal.map.source_group,TodaPrimaryGroup(8,5))
    assert not expand_finite_delta_injective(MapInjective(invalid),domain,replace(image,map=invalid),order)
    e = TodaSuspensionMap(goal.map.source_group,goal.map.target_group)
    assert not expand_finite_delta_injective(MapInjective(e),domain,replace(image,map=e),order)


def test_require_real_premise_shapes_and_inference_trust():
    goal, domain, codomain, image, order = fixture()
    first, = expand_summand_generator_order(order,codomain)
    second, = expand_finite_delta_injective(goal,domain,image,order)
    assert not find_inference_matches_for_rule(first.rule,(hypothetical(codomain,ProofRule.RELATION),))
    d,i,o = hypothetical(domain),hypothetical(image),hypothetical(order)
    for parents in ((d,i),(d,o),(d,hypothetical(image,ProofRule.GIVEN),o),
                    (d,i,hypothetical(order,ProofRule.GIVEN)),
                    (hypothetical(domain,ProofRule.RELATION),i,o),
                    (d,i,hypothetical(replace(order,order=4)))):
        assert not find_inference_matches_for_rule(second.rule,parents)
