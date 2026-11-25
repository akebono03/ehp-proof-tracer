"""Verify the actual source-first public path, without injecting proof steps."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum, Suspension
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r7_left_composition_reuse_audit.audit import public_search
from phase177_r9_delta_rhs_normalization_audit.audit import canonical_delta, probe_goals, route_matches
from phase177_r10_composition_associativity_isolated.rule import (
    RULE_NAME, expand_composition_associativity_equality,
    ordered_composition_factors,
)
from proof import ProofRule, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from relation_rules import equality_symmetry_inference_rule


def verify_associativity(step, target):
    """Verify a direct rule or the same rule followed by existing symmetry."""
    assert step.conclusion == target and step.rule is ProofRule.INFERENCE
    assert step.inference_rule is not None
    if step.inference_rule.name == 'equality symmetry':
        witness, = step.premises
        assert witness.conclusion == Relation(target.rhs, target.lhs)
        matches = find_inference_matches_for_rule(equality_symmetry_inference_rule(), (witness,))
        assert any(apply_inference_match(m).conclusion == target and m.premises == (witness,) for m in matches)
    else:
        witness = step
    assert witness.rule is ProofRule.INFERENCE
    assert witness.inference_rule is not None and witness.inference_rule.name == RULE_NAME
    assert not witness.premises
    option, = expand_composition_associativity_equality(witness.conclusion)
    assert option.subgoals == ()
    matches = find_inference_matches_for_rule(option.rule, ())
    assert any(apply_inference_match(m).conclusion == witness.conclusion and not m.premises for m in matches)


@pytest.fixture(scope='module')
def context():
    invocation, result, calls, model, view = capture()
    assert model is not None and invocation['goal'].lhs == result.target
    print('PHASE177_R11_ROOT_STATUS='+result.status.value)
    print('PHASE177_R11_ROOT_OPEN_GOALS='+str(len(result.open_goals)))
    return invocation


def targets(context):
    root = context['goal']
    routes = expand_public_two_summand_quotient(
        CyclicStructureStatement(root.lhs, root.rhs.generator, 2), proof_target=root)
    assert len(routes) == 2
    values = [delta_image_equality(route.subgoals[2]) for route in routes]
    assert all(value is not None for value in values)
    canonical = canonical_delta()
    actual, = [value for value in values if route_matches(canonical, value)]
    other, = [value for value in values if value != actual]
    probes = probe_goals(canonical, actual)
    return probes, Relation(probes['notation_only_delta'].rhs, actual.rhs), other


def fresh(context):
    return shared_expansion_provider(context['bridge'], proof_target=context['goal'])


def prove(target, context, provider):
    assert any(o.rule.name == RULE_NAME and o.subgoals == () for o in provider(target))
    step, row = public_search(target, context, provider)
    assert step is not None, row
    verify_associativity(step, target)


@pytest.mark.parametrize('label', ['generic_associativity', 'canonical_associativity', 'reverse_associativity', 'db_associativity'])
def test_public_associativity(label, context):
    probes, db, _ = targets(context)
    target = db if label == 'db_associativity' else probes[label]
    prove(target, context, fresh(context))
    print('PHASE177_R11_CASE='+label+':PUBLIC_ASSOCIATIVITY_PROVED')


@pytest.mark.parametrize('kind', ['four_factors', 'suspension', 'iterated', 'sum', 'multiple'])
def test_general_typed_factors(kind, context):
    a = HomotopyElement('a',3,5,3)
    b = HomotopyElement('b',5,6,5)
    c = HomotopyElement('c',6,9,6)
    if kind == 'four_factors':
        d = HomotopyElement('d',9,10,9)
        target = Relation(Composition(Composition(a,b),Composition(c,d)),
                          Composition(a,Composition(b,Composition(c,d))))
    else:
        if kind == 'suspension':
            a,b,c = (Suspension(x) for x in (a,b,c))
        elif kind == 'iterated':
            a,b,c = (IteratedSuspension(x,2) for x in (a,b,c))
        elif kind == 'sum':
            a = Sum(a,a)
        else:
            a = Multiple(3,a)
        target = Relation(Composition(Composition(a,b),c), Composition(a,Composition(b,c)))
    prove(target, context, fresh(context))
    print('PHASE177_R11_CASE='+kind+':PUBLIC_ASSOCIATIVITY_PROVED')


def test_public_rejects_wrong_factors(context):
    probes, db, other = targets(context)
    wrong = Relation(db.lhs, other.rhs)
    a,b,c = ordered_composition_factors(db.lhs)
    bad = (wrong, Relation(db.lhs, db.lhs), replace(db, relation_type=RelationType.ORDER),
           Relation(db.lhs, Composition(b,Composition(a,c))), probes['entire_rhs_equality'])
    provider = fresh(context)
    for target in bad:
        assert not any(o.rule.name == RULE_NAME for o in provider(target))
    assert not expand_composition_associativity_equality(wrong)


def test_captured_actual_db_associativity(context):
    _, target, _ = targets(context)
    prove(target, context, context['expansion_provider'])
    print('PHASE177_R11_CAPTURED_DB_ASSOCIATIVITY_PROVED=TRUE')


def test_observe_remaining_delta_frontier(context):
    probes, db, _ = targets(context)
    first, first_row = public_search(probes['notation_only_delta'], context, fresh(context))
    assert first is not None and first.rule is ProofRule.INFERENCE, first_row
    step, row = public_search(probes['actual_delta'], context, fresh(context))
    if step is not None:
        assert step.rule is ProofRule.INFERENCE
    print('PHASE177_R11_ACTUAL_DELTA='+('PROVED' if step is not None else 'OPEN'))
