"""Check general proposals and real source-first Delta proof trees."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum, Suspension
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME as DELTA_RULE
from phase177_r7_left_composition_reuse_audit.audit import public_search
from phase177_r10_composition_associativity_isolated.rule import is_composition_associativity_equality
from phase177_r11_composition_associativity_public.tests.test_public import targets, verify_associativity
from phase177_r12_reassociation_transitivity_public.provider import (
    expand_public_reassociation_transitivity, reassociation_inputs,
)
from proof import ProofRule, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from relation_rules import equality_transitivity_inference_rule


def ancestors(step):
    yield step
    for parent in step.premises:
        yield from ancestors(parent)


@pytest.mark.parametrize('kind', ['three', 'four', 'suspension', 'iterated', 'sum', 'multiple'])
def test_generic_candidate(kind):
    a = HomotopyElement('a',3,5,3)
    b = HomotopyElement('b',5,6,5)
    c = HomotopyElement('c',6,9,6)
    if kind == 'suspension':
        a,b,c = (Suspension(x) for x in (a,b,c))
    elif kind == 'iterated':
        a,b,c = (IteratedSuspension(x,2) for x in (a,b,c))
    elif kind == 'sum':
        a = Sum(a,a)
    elif kind == 'multiple':
        a = Multiple(2,a)
    middle, right = Composition(Composition(a,b),c), Composition(a,Composition(b,c))
    if kind == 'four':
        d = HomotopyElement('d',9,10,9)
        middle = Composition(middle,d)
        right = Composition(a,Composition(b,Composition(c,d)))
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    source,target = typed_endpoints(right)
    lhs = HomotopyElement('independent',target,source,target)
    goal = Relation(lhs,right)
    expected = (Relation(lhs,middle), Relation(middle,right))
    assert reassociation_inputs(goal) == expected
    option, = expand_public_reassociation_transitivity(goal)
    assert option.rule.name == 'equality transitivity'
    assert option.subgoals == expected
    assert is_composition_associativity_equality(expected[1])
    assert not expand_public_reassociation_transitivity(expected[0])
    assert not expand_public_reassociation_transitivity(expected[1])
    assert not find_inference_matches_for_rule(option.rule, ())


def test_rejects_invalid_and_no_progress():
    a = HomotopyElement('a',3,5,3)
    b = HomotopyElement('b',5,6,5)
    c = HomotopyElement('c',6,9,6)
    lhs = HomotopyElement('independent',3,9,3)
    right = Composition(a,Composition(b,c))
    middle = Composition(Composition(a,b),c)
    goal = Relation(lhs,right)
    bad = (Relation(lhs,middle), Relation(middle,right), Relation(right,right),
           Relation(lhs,Composition(a,b)), Relation(lhs,Composition(a,Composition(replace(b,source=7),c))),
           replace(goal,relation_type=RelationType.ORDER), replace(goal,note='annotation'), object())
    for item in bad:
        assert reassociation_inputs(item) is None
        assert not expand_public_reassociation_transitivity(item)


@pytest.fixture(scope='module')
def context():
    invocation, result, calls, model, view = capture()
    assert invocation['goal'].lhs == result.target
    print('PHASE177_R12_ROOT_STATUS='+result.status.value)
    print('PHASE177_R12_ROOT_OPEN_GOALS='+str(len(result.open_goals)))
    print('PHASE177_R12_WEB_KEY='+view.key)
    return invocation


def fresh(context):
    return shared_expansion_provider(context['bridge'], proof_target=context['goal'])


def verify_transport(step, target, intermediate):
    assert step.conclusion == target and step.rule is ProofRule.INFERENCE
    expected = (intermediate, Relation(intermediate.rhs,target.rhs))
    for node in ancestors(step):
        if (node.conclusion != target or node.rule is not ProofRule.INFERENCE
                or node.inference_rule is None or node.inference_rule.name != 'equality transitivity'
                or tuple(p.conclusion for p in node.premises) != expected):
            continue
        first, second = node.premises
        assert first.rule is ProofRule.INFERENCE and second.rule is ProofRule.INFERENCE
        verify_associativity(second, expected[1])
        nodes = tuple(ancestors(first))
        assert any(p.rule is ProofRule.INFERENCE and p.inference_rule is not None
                   and p.inference_rule.name == DELTA_RULE for p in nodes)
        for citation in (CitedTodaProp25(), CitedToda511(canonical_511())):
            assert any(p.rule is ProofRule.GIVEN and not p.premises and p.conclusion == citation for p in nodes)
        matches = find_inference_matches_for_rule(equality_transitivity_inference_rule(),node.premises)
        assert any(apply_inference_match(m).conclusion == target and m.premises == node.premises for m in matches)
        return
    pytest.fail('Missing exact independently proved transitivity parents')


@pytest.mark.parametrize('label,intermediate_label', [('reassociated_delta','canonical_delta'), ('actual_delta','notation_only_delta')])
def test_public_delta_transport(label, intermediate_label, context):
    probes, _, _ = targets(context)
    target, intermediate = probes[label], probes[intermediate_label]
    provider = fresh(context)
    expected = (intermediate, Relation(intermediate.rhs,target.rhs))
    assert reassociation_inputs(target) == expected
    assert any(o.rule.name == 'equality transitivity' and o.subgoals == expected for o in provider(target))
    step,row = public_search(target,context,provider)
    assert step is not None, row
    verify_transport(step,target,intermediate)
    print('PHASE177_R12_CASE='+label+':PUBLIC_DELTA_PROVED')


def test_captured_actual_delta(context):
    probes, _, _ = targets(context)
    target, intermediate = probes['actual_delta'], probes['notation_only_delta']
    step,row = public_search(target,context,context['expansion_provider'])
    assert step is not None, row
    verify_transport(step,target,intermediate)
    print('PHASE177_R12_CAPTURED_ACTUAL_DELTA_PROVED=TRUE')


def test_other_route_not_proved_by_reassociation(context):
    probes, _, other = targets(context)
    assert not is_composition_associativity_equality(Relation(probes['notation_only_delta'].rhs,other.rhs))
    step,row = public_search(other,context,fresh(context))
    assert step is None, row
    print('PHASE177_R12_OTHER_DELTA_ROUTE=OPEN')
