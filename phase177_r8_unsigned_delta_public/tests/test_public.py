"""Replay actual source-first derivations and observe the remaining root frontier."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME, expand_unsigned_prop25
from phase177_r4_general_iterated_suspension_audit.audit import cases
from phase177_r7_left_composition_reuse_audit.audit import public_search
from phase177_r8_unsigned_delta_public.provider import expand_public_unsigned_delta
from proof import ProofRule, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule


def canonical_targets():
    base = canonical_511()
    beta, _, gamma = cases()['eta']
    explicit = Composition(base.lhs.expression, IteratedSuspension(beta, 2))
    named = Composition(base.lhs.expression, gamma)
    rhs = Composition(base.rhs, beta)
    return base, Relation(MapApplication(EHP_DELTA_MAP, explicit), rhs), Relation(MapApplication(EHP_DELTA_MAP, named), rhs)


def test_cited_source_and_independent_identity_obligations():
    base, literal, named = canonical_targets()
    sources = (CitedTodaProp25(), CitedToda511(base))
    a, = expand_public_unsigned_delta(literal, sources)
    b, = expand_public_unsigned_delta(named, sources)
    assert a.rule.name == b.rule.name == RULE_NAME
    assert a.subgoals == (CitedTodaProp25(), base)
    assert b.subgoals == (CitedTodaProp25(), base, Relation(literal.lhs.expression, named.lhs.expression))
    for missing in ((), sources[:1], sources[1:]):
        assert not expand_public_unsigned_delta(named, missing)
    assert not expand_public_unsigned_delta(named, sources + sources[:1])
    assert not expand_public_unsigned_delta(replace(named, lhs=MapApplication(EHP_H_MAP, named.lhs.expression)), sources)
    assert not expand_public_unsigned_delta(replace(named, relation_type=RelationType.ORDER), sources)


@pytest.mark.parametrize('m,i,j,valid', [(3,6,10,True), (4,9,10,True), (4,9,11,False)])
def test_generic_base_candidates(m,i,j,valid):
    a = HomotopyElement('a', 2*m+1, i+1, 2*m+1)
    b = HomotopyElement('b', i-1, j-1, i-1)
    x = HomotopyElement('x', m, i-1, m)
    base = Relation(MapApplication(EHP_DELTA_MAP, a), x)
    goal = Relation(MapApplication(EHP_DELTA_MAP, Composition(a, IteratedSuspension(b,2))), Composition(x,b))
    options = expand_public_unsigned_delta(goal, (CitedTodaProp25(),), (base,))
    assert bool(options) is valid
    if valid:
        assert options[0].subgoals == (CitedTodaProp25(), base)
        assert options[0].rule.name == RULE_NAME
    assert not expand_public_unsigned_delta(goal, (), (base,))


@pytest.fixture(scope='module')
def context():
    invocation, result, calls, model, view = capture()
    assert model is not None and invocation['goal'].lhs == result.target
    print('PHASE177_R8_ROOT_STATUS='+result.status.value)
    print('PHASE177_R8_ROOT_OPEN_GOALS='+str(len(result.open_goals)))
    print('PHASE177_R8_WEB_KEY='+view.key)
    return invocation


def ancestors(step):
    yield step
    for parent in step.premises:
        yield from ancestors(parent)


def verify_unsigned(step, target, base, identity):
    """Do not require a particular final rule if the checked R3 node exists."""
    required, = expand_unsigned_prop25(target, base, identity)
    for node in ancestors(step):
        if (node.conclusion != target or node.rule is not ProofRule.INFERENCE
                or node.inference_rule is None or node.inference_rule.name != RULE_NAME):
            continue
        assert tuple(p.conclusion for p in node.premises) == required.subgoals
        assert node.premises[0].rule is ProofRule.GIVEN and not node.premises[0].premises
        assert all(p.rule is ProofRule.INFERENCE for p in node.premises[1:])
        assert any(p.rule is ProofRule.GIVEN and p.conclusion == CitedToda511(base)
                   for p in ancestors(node.premises[1]))
        matches = find_inference_matches_for_rule(required.rule, node.premises)
        assert any(apply_inference_match(match).conclusion == target
                   and match.premises == node.premises for match in matches)
        return
    pytest.fail('Missing checked unsigned Prop 2.5 node for exact goal')


@pytest.mark.parametrize('label', ['literal','named'])
def test_public_delta(label, context):
    base, literal, named = canonical_targets()
    target = literal if label == 'literal' else named
    identity = None if label == 'literal' else Relation(literal.lhs.expression, named.lhs.expression)
    available = screened_cited_facts(context['bridge'])
    assert CitedTodaProp25() in available and CitedToda511(base) in available
    provider = shared_expansion_provider(context['bridge'], proof_target=context['goal'])
    required, = expand_unsigned_prop25(target, base, identity)
    assert any(o.rule.name == RULE_NAME and o.subgoals == required.subgoals for o in provider(target))
    step, row = public_search(target, context, provider)
    assert step is not None, row
    assert step.rule is ProofRule.INFERENCE
    verify_unsigned(step, target, base, identity)
    print('PHASE177_R8_CASE='+label+':PUBLIC_DELTA_PROVED')


def test_actual_captured_named_goal(context):
    base, literal, named = canonical_targets()
    step, row = public_search(named, context, context['expansion_provider'])
    assert step is not None, row
    verify_unsigned(step, named, base, Relation(literal.lhs.expression, named.lhs.expression))
    print('PHASE177_R8_CAPTURED_NAMED_DELTA_PROVED=TRUE')


def test_observe_actual_quotient_routes(context):
    """Independent route probes are not evidence for the original root run."""
    root = context['goal']
    routes = expand_public_two_summand_quotient(
        CyclicStructureStatement(root.lhs, root.rhs.generator, 2), proof_target=root)
    assert len(routes) == 2
    for index, route in enumerate(routes):
        target = delta_image_equality(route.subgoals[2])
        assert target is not None
        provider = shared_expansion_provider(context['bridge'], proof_target=root)
        step, row = public_search(target, context, provider)
        if step is not None:
            assert step.rule is ProofRule.INFERENCE
        print('PHASE177_R8_ACTUAL_ROUTE_'+str(index)+'='+('PROVED' if step is not None else 'OPEN'))
        print('PHASE177_R8_ACTUAL_ROUTE_'+str(index)+'_GOAL='+repr(target))
