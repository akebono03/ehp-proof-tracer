"""Exercise actual public search and verify the candidate-only boundary."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, Suspension
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r4_general_iterated_suspension_audit.audit import cases, goals, image
from phase177_r5_general_suspension_equality_isolated.rule import (
    IMAGE_RULE, NOTATION_RULE, expand_iterated_notation_equality,
)
from phase177_r6_general_suspension_public.provider import (
    expand_public_suspension_equality, middle_candidates, structural_middle,
)
from proof import (
    ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule,
)
from relation_rules import equality_symmetry_inference_rule


@pytest.fixture(scope='module')
def invocation():
    context, result, calls, model, view = capture()
    assert model is not None and context['goal'].lhs == result.target
    print('PHASE177_R6_ROOT_STATUS='+result.status.value)
    print('PHASE177_R6_ROOT_OPEN_GOALS='+str(len(result.open_goals)))
    return context


def prove(goal, context, *, captured=False):
    provider = (context['expansion_provider'] if captured else
                shared_expansion_provider(context['bridge'], proof_target=context['goal']))
    step = reconstruct_registered_goal(
        goal, context['bridge'], context['citing_assertion_id'], provider,
        lookup_mode=context['lookup_mode'],
        verified_assertion_ids=context.get('verified_assertion_ids', ()),
        completed_internal_proofs=context.get('completed_internal_proofs', ()),
    )
    assert step.conclusion == goal and step.rule is ProofRule.INFERENCE
    return step


def ancestors(step):
    yield step
    for parent in step.premises:
        yield from ancestors(parent)


@pytest.mark.parametrize('label', ['eta','nu_cited','sigma_cited','epsilon_cited'])
def test_public_double_equality(label, invocation):
    values = cases()[label]
    target = goals(*values)['double_equality']
    step = prove(target, invocation)
    names = {p.inference_rule.name for p in ancestors(step) if p.inference_rule is not None}
    assert NOTATION_RULE in names
    assert 'equality transitivity' in names
    assert 'suspension preserves equality' in names
    if label != 'eta':
        assert IMAGE_RULE in names
    print('PHASE177_R6_CASE='+label+':DOUBLE_EQUALITY_PROVED')


@pytest.mark.parametrize('label', ['formal_stable','formal_unstable'])
def test_public_formal_notation(label, invocation):
    target = goals(*cases()[label])['nested_to_iterated']
    step = prove(target, invocation)
    # First Successful Proof Search may use the direct definition or
    # its reverse followed by the existing equality symmetry rule.
    assert step.inference_rule is not None
    if step.inference_rule.name == 'equality symmetry':
        witness, = step.premises
        assert witness.conclusion == Relation(target.rhs, target.lhs)
        assert witness.rule is ProofRule.INFERENCE
        match, = find_inference_matches_for_rule(
            equality_symmetry_inference_rule(), (witness,),
        )
        verified = apply_inference_match(match)
        assert verified.conclusion == target
        assert verified.premises == (witness,)
    else:
        witness = step
        assert witness.conclusion == target
    assert witness.rule is ProofRule.INFERENCE
    assert witness.inference_rule is not None
    assert witness.inference_rule.name == NOTATION_RULE
    assert not witness.premises
    # Check the actual terminal witness against the isolated R5 rule;
    # a matching rule name alone is not sufficient evidence.
    option, = expand_iterated_notation_equality(witness.conclusion)
    assert option.subgoals == ()
    match, = find_inference_matches_for_rule(option.rule, ())
    verified = apply_inference_match(match)
    assert verified.conclusion == witness.conclusion
    assert verified.rule is ProofRule.INFERENCE and not verified.premises
    print('PHASE177_R6_CASE='+label+':FORMAL_NOTATION_PROVED')


def test_actual_captured_provider_proves_eta_double(invocation):
    target = goals(*cases()['eta'])['double_equality']
    prove(target, invocation, captured=True)


def test_nonregistered_middle_from_candidate_image_only():
    x = HomotopyElement('x',3,6,3)
    y = HomotopyElement('y',4,7,4)
    z = HomotopyElement('z',5,8,5)
    target = Relation(IteratedSuspension(x,2), z)
    assert not expand_public_suspension_equality(target)
    witness = image(x,y)
    assert middle_candidates(x,z,(witness,)) == (y,)
    root, = expand_public_suspension_equality(target,(witness,))
    nested = Suspension(Suspension(x))
    assert root.subgoals == (Relation(target.lhs,nested), Relation(nested,z))
    child = expand_public_suspension_equality(Relation(nested,z),(witness,))
    assert child[0].subgoals == (Relation(nested,Suspension(y)), Relation(Suspension(y),z))
    # Availability is not a proof: the second E-image remains an explicit obligation.
    second, = expand_public_suspension_equality(Relation(Suspension(y),z),(witness,))
    assert second.subgoals == (image(y,z),)


def test_structural_composite_candidates():
    x,y,z = cases()['eta']
    # x: 9 -> 8, y: 10 -> 9, z: 11 -> 10; use another consecutive member.
    from phase177_r4_general_iterated_suspension_audit.audit import family_member
    from phase169_r10b_registered_stable_family_binding.family_registry import registered_family_of
    family = registered_family_of(z)
    t = family_member(family,11)
    assert structural_middle(Composition(x,y), Composition(z,t)) == Composition(y,z)


def test_wrong_family_and_wrong_dimensions_not_guessed():
    x, y, z = cases()['eta']
    bad = replace(z, name='other')
    assert not middle_candidates(x,bad,())
    assert not expand_public_suspension_equality(Relation(IteratedSuspension(x,2),bad))
    assert not expand_public_suspension_equality(Relation(IteratedSuspension(x,2),y))
    assert not expand_public_suspension_equality(Relation(IteratedSuspension(x,True),z))
