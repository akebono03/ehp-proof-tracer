"""Check general associativity and replay the actual R8 Delta proof with it."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum, Suspension
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase175_r4r12r10r1_cited_511_public.source import canonical_511
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import same_typed_generator_notation
from phase176_r3r50_strict_nu_prime_connection.notation import strict_nu_prime_alias
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r4_general_iterated_suspension_audit.audit import cases
from phase177_r7_left_composition_reuse_audit.audit import public_search
from phase177_r10_composition_associativity_isolated.rule import (
    RULE_NAME, expand_composition_associativity_equality,
    is_composition_associativity_equality, ordered_composition_factors,
)
from proof import ProofRule, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from relation_rules import equality_transitivity_inference_rule


def replay(rule, parents, goal):
    matches = find_inference_matches_for_rule(rule, parents)
    steps = [apply_inference_match(match) for match in matches]
    step, = [s for s in steps if s.conclusion == goal and s.premises == parents]
    assert step.rule is ProofRule.INFERENCE
    return step


def prove_associativity(goal):
    option, = expand_composition_associativity_equality(goal)
    assert option.rule.name == RULE_NAME and option.subgoals == ()
    return replay(option.rule, (), goal)


def chain(sphere):
    a = HomotopyElement('a', sphere, sphere+3, sphere)
    b = HomotopyElement('b', sphere+3, sphere+4, sphere+3)
    c = HomotopyElement('c', sphere+4, sphere+6, sphere+4)
    return a,b,c


@pytest.mark.parametrize('sphere', [2,3,5,17])
@pytest.mark.parametrize('reverse', [False,True])
def test_generic_typed_associativity(sphere, reverse):
    a,b,c = chain(sphere)
    lhs, rhs = Composition(Composition(a,b),c), Composition(a,Composition(b,c))
    if reverse:
        lhs,rhs = rhs,lhs
    assert ordered_composition_factors(lhs) == ordered_composition_factors(rhs) == (a,b,c)
    assert typed_endpoints(lhs) == typed_endpoints(rhs) == (sphere+6,sphere)
    prove_associativity(Relation(lhs,rhs))


@pytest.mark.parametrize('kind', ['suspension','iterated','sum','multiple'])
def test_non_atomic_typed_factors(kind):
    a,b,c = chain(3)
    if kind == 'suspension':
        a,b,c = (Suspension(x) for x in (a,b,c))
    elif kind == 'iterated':
        a,b,c = (IteratedSuspension(x,2) for x in (a,b,c))
    elif kind == 'sum':
        a = Sum(a,a)
    else:
        a = Multiple(2,a)
    prove_associativity(Relation(Composition(Composition(a,b),c), Composition(a,Composition(b,c))))


def test_four_factors_change_parentheses_only():
    a,b,c = chain(3)
    d = HomotopyElement('d',9,11,9)
    lhs = Composition(Composition(a,b),Composition(c,d))
    rhs = Composition(a,Composition(Composition(b,c),d))
    assert ordered_composition_factors(lhs) == (a,b,c,d)
    prove_associativity(Relation(lhs,rhs))


def test_rejects_reordered_replaced_untyped_or_reflexive_factors():
    a,b,c = (HomotopyElement(name,4,4,4) for name in ('a','b','c'))
    lhs = Composition(Composition(a,b),c)
    right = Composition(a,Composition(b,c))
    wrong = replace(b,source=5)
    bad = (Relation(lhs,Composition(b,Composition(a,c))),
           Relation(lhs,Composition(a,Composition(replace(b,name='other'),c))),
           Relation(lhs,Composition(a,Composition(wrong,c))),
           Relation(lhs,lhs), Relation(a,a),
           Relation(lhs,right,RelationType.ORDER),
           replace(Relation(lhs,right),note='not plain equality'),
           Relation(Composition(Composition(a,IteratedSuspension(b,True)),c),right),
           Relation(Composition(Composition(a,IteratedSuspension(b,-1)),c),right))
    for goal in bad:
        assert not is_composition_associativity_equality(goal)
        assert not expand_composition_associativity_equality(goal)
    assert ordered_composition_factors(Composition(a,Composition(wrong,c))) is None
    assert not expand_composition_associativity_equality(object())


def test_does_not_normalize_suspension_or_symbol_aliases():
    a,b,c = chain(3)
    a,b,c = (Suspension(x) for x in (a,b,c))
    lhs = Composition(Composition(a,b),c)
    rhs = Composition(IteratedSuspension(a.expression,1),Composition(b,c))
    assert typed_endpoints(lhs) == typed_endpoints(rhs)
    assert not expand_composition_associativity_equality(Relation(lhs,rhs))


@pytest.fixture(scope='module')
def invocation():
    context, result, calls, model, view = capture()
    assert model is not None and context['goal'].lhs == result.target
    return context


def test_actual_db_delta_rhs_reassociation_replays_with_real_proof(invocation):
    root = invocation['goal']
    routes = expand_public_two_summand_quotient(
        CyclicStructureStatement(root.lhs,root.rhs.generator,2), proof_target=root)
    assert len(routes) == 2
    base = canonical_511()
    beta,_,gamma = cases()['eta']
    from expression import MapApplication
    from map_facts import EHP_DELTA_MAP
    canonical = Relation(MapApplication(EHP_DELTA_MAP,Composition(base.lhs.expression,gamma)),
                         Composition(base.rhs,beta))
    a,b,c = ordered_composition_factors(canonical.rhs)
    matched = []
    for route in routes:
        target = delta_image_equality(route.subgoals[2])
        assert target is not None
        factors = ordered_composition_factors(target.rhs)
        if (target.lhs == canonical.lhs and factors is not None and len(factors) == 3
                and factors[1:] == (b,c) and type(factors[0]) is IteratedSuspension
                and type(factors[0].exponent) is int and factors[0].exponent == 1
                and strict_nu_prime_alias(a.expression,factors[0].expression)
                and same_typed_generator_notation(a,factors[0])):
            matched.append((target,factors[0]))
    (target,d), = matched
    assert target.rhs == Composition(d,Composition(b,c))
    intermediate = Relation(target.lhs,Composition(Composition(d,b),c))
    provider = shared_expansion_provider(invocation['bridge'],proof_target=root)
    first,row = public_search(intermediate,invocation,provider)
    assert first is not None, row
    assert first.rule is ProofRule.INFERENCE and first.conclusion == intermediate
    equality = Relation(intermediate.rhs,target.rhs)
    second = prove_associativity(equality)
    final = replay(equality_transitivity_inference_rule(),(first,second),target)
    assert final.premises == (first,second)
    # Isolated replay only: the original root and public search are untouched.
    print('PHASE177_R10_ACTUAL_DB_DELTA_ISOLATED_REPLAY=PROVED')
    other, = [delta_image_equality(r.subgoals[2]) for r in routes
              if delta_image_equality(r.subgoals[2]) != target]
    assert not expand_composition_associativity_equality(Relation(intermediate.rhs,other.rhs))
