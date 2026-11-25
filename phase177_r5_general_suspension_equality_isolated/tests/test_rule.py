from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum, Suspension
from phase177_r4_general_iterated_suspension_audit.audit import cases, image
from phase177_r5_general_suspension_equality_isolated.rule import (
    expand_iterated_notation_equality, expand_suspension_image_equality,
    suspension_image_input,
)
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from proof import (ProofRule, ProofStep, Relation, RelationType,
                   apply_inference_match, find_inference_matches_for_rule)
from relation_rules import (equality_transitivity_inference_rule,
                            suspension_preserves_equality_inference_rule)


def replay(rule, parents, goal):
    matches = find_inference_matches_for_rule(rule, parents)
    valid = [apply_inference_match(m) for m in matches]
    matching = [s for s in valid if s.conclusion == goal and s.premises == parents]
    assert len(matching) == 1
    assert matching[0].rule is ProofRule.INFERENCE
    return matching[0]


def infer(options, parents, goal):
    option, = options
    assert option.subgoals == tuple(p.conclusion for p in parents)
    return replay(option.rule, parents, goal)


@pytest.fixture(scope='module')
def context():
    invocation, result, calls, model, view = capture()
    assert model is not None and invocation['goal'].lhs == result.target
    return invocation


def prove_image(goal, invocation):
    provider = shared_expansion_provider(invocation['bridge'], proof_target=invocation['goal'])
    step = reconstruct_registered_goal(
        goal, invocation['bridge'], invocation['citing_assertion_id'], provider,
        lookup_mode=invocation['lookup_mode'],
        verified_assertion_ids=invocation.get('verified_assertion_ids', ()),
        completed_internal_proofs=invocation.get('completed_internal_proofs', ()),
    )
    assert step.conclusion == goal and step.rule is ProofRule.INFERENCE
    return step


@pytest.mark.parametrize('label', ['eta','nu_cited','sigma_cited','epsilon_cited'])
def test_real_existing_images_imply_double_suspension(label, context):
    x, y, z = cases()[label]
    p, q = prove_image(image(x, y), context), prove_image(image(y, z), context)
    first, second = Relation(Suspension(x), y), Relation(Suspension(y), z)
    a = infer(expand_suspension_image_equality(first), (p,), first)
    b = infer(expand_suspension_image_equality(second), (q,), second)
    nested = Suspension(Suspension(x))
    shifted = Relation(nested, Suspension(y))
    c = replay(suspension_preserves_equality_inference_rule(), (a,), shifted)
    nested_eq = Relation(nested, z)
    d = replay(equality_transitivity_inference_rule(), (c,b), nested_eq)
    notation = Relation(IteratedSuspension(x,2), nested)
    e = infer(expand_iterated_notation_equality(notation), (), notation)
    final = Relation(IteratedSuspension(x,2), z)
    step = replay(equality_transitivity_inference_rule(), (e,d), final)
    assert step.premises == (e,d)


@pytest.mark.parametrize('label', ['formal_stable','formal_unstable'])
def test_formal_notation_without_stable_range(label):
    x, _, _ = cases()[label]
    for p,q in [(1,1),(2,3),(4,7)]:
        a = IteratedSuspension(IteratedSuspension(x,p),q)
        b = IteratedSuspension(x,p+q)
        for goal in (Relation(a,b), Relation(b,a)):
            infer(expand_iterated_notation_equality(goal), (), goal)
    g = Relation(Suspension(Suspension(x)), IteratedSuspension(x,2))
    infer(expand_iterated_notation_equality(g), (), g)


def test_formal_composite_sum_multiple():
    a = HomotopyElement('a',3,6,3)
    b = HomotopyElement('b',6,7,6)
    c = Composition(a,b)
    for x in (c, Sum(a,a), Multiple(3,a)):
        g = Relation(Suspension(Suspension(x)), IteratedSuspension(x,2))
        infer(expand_iterated_notation_equality(g), (), g)


def test_image_requires_exact_independent_inferred_witness():
    x, y, z = cases()['eta']
    goal = Relation(Suspension(x),y)
    option, = expand_suspension_image_equality(goal)
    p, = option.subgoals
    assert p == image(x,y)
    assert not find_inference_matches_for_rule(option.rule, ())
    for witness in (ProofStep(p, (), ProofRule.GIVEN),
                    ProofStep(replace(p,target_generator=replace(y,name='other')), (), ProofRule.INFERENCE),
                    ProofStep(replace(p,map=image(y,z).map), (), ProofRule.INFERENCE)):
        assert not find_inference_matches_for_rule(option.rule, (witness,))
    assert suspension_image_input(Relation(Suspension(x),z)) is None
    assert not expand_suspension_image_equality(Relation(y,Suspension(x)))
    assert not expand_suspension_image_equality(replace(goal,relation_type=RelationType.ORDER))


def test_rejects_unrelated_or_malformed_notation():
    x,_,_ = cases()['formal_unstable']
    nested = Suspension(Suspension(x))
    for rhs in (IteratedSuspension(replace(x,name='other'),2), IteratedSuspension(x,3),
                IteratedSuspension(x,True), IteratedSuspension(x,-2), nested):
        assert not expand_iterated_notation_equality(Relation(nested,rhs))
    invalid = replace(x,dimension=x.dimension+1)
    assert not expand_iterated_notation_equality(Relation(Suspension(Suspension(invalid)),IteratedSuspension(invalid,2)))
    assert not expand_iterated_notation_equality(Relation(Suspension(x),IteratedSuspension(x,1)))
