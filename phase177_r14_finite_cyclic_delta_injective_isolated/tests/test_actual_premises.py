"""Replay only the isolated rules with actual cited/authorized prior premises."""
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, exact_prior_database_result, verified_db_step
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase175_r4r12r10r1_cited_511_public.provider import same_registered_cited_511
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r7_left_composition_reuse_audit.audit import public_search
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import (
    ORDER_RULE, INJECTIVE_RULE, expand_summand_generator_order, expand_finite_delta_injective,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule


def replay(option, parents, target):
    matches = find_inference_matches_for_rule(option.rule,parents)
    step, = tuple(apply_inference_match(m) for m in matches if m.premises == parents)
    assert step.conclusion == target and step.rule is ProofRule.INFERENCE
    assert step.premises == parents
    return step


def ancestors(step):
    yield step
    for parent in step.premises:
        yield from ancestors(parent)


def test_actual_lower_delta_isolated_replay():
    invocation,result,calls,model,view = capture()
    root,bridge = invocation['goal'],invocation['bridge']
    assert root.lhs == result.target == TodaPrimaryGroup(10,5)
    assert model is not None
    domain = exact_prior_database_result(9,1)
    codomain = exact_prior_database_result(4,4)
    assert isinstance(domain.rhs,FiniteCyclicGroup) and domain.rhs.order == 2
    assert isinstance(codomain.rhs,DirectSumGroup)
    delta = TodaDeltaMap(domain.lhs,codomain.lhs)
    target = MapInjective(delta)
    images = [GeneratorImage(delta,domain.rhs.generator,p.generator)
              for p in codomain.rhs.summands if isinstance(p,FiniteCyclicGroup)]
    image, = [g for g in images if delta_image_equality(g) is not None
              and same_registered_cited_511(delta_image_equality(g))]
    order = FiniteElementOrder(codomain.lhs,image.target_generator,domain.rhs.order)
    provider = shared_expansion_provider(bridge,proof_target=root)
    assert all(o.rule.name != INJECTIVE_RULE for o in provider(target))
    assert all(o.rule.name != ORDER_RULE for o in provider(order))
    domain_step, domain_row = public_search(domain,invocation,provider)
    assert domain_step is not None, domain_row
    image_step, image_row = public_search(image,invocation,provider)
    assert image_step is not None and image_step.rule is ProofRule.INFERENCE, image_row
    assert any(s.rule is ProofRule.GIVEN and s.conclusion == CitedToda511(canonical_511())
               for s in ancestors(image_step))
    # Explicitly use the existing root-context DB admission gate, not an invented
    # proof or a public DFS success. R13's independent codomain search was open.
    codomain_step = admitted_db_step(codomain,proof_target=root,bridge=bridge)
    assert codomain_step is not None
    assert verified_db_step(codomain_step,proof_target=root,bridge=bridge)
    first, = expand_summand_generator_order(order,codomain)
    order_step = replay(first,(codomain_step,),order)
    second, = expand_finite_delta_injective(target,domain,image,order)
    replay(second,(domain_step,image_step,order_step),target)
    print('PHASE177_R14_CODOMAIN=VERIFIED_DB_ADMISSION_NOT_PUBLIC_SEARCH')
    print('PHASE177_R14_ACTUAL_CITED_GENERATOR_IMAGE=PROVED_INFERENCE')
    print('PHASE177_R14_ACTUAL_IMAGE_ORDER=ISOLATED_PROVED')
    print('PHASE177_R14_ACTUAL_DELTA_INJECTIVE=ISOLATED_PROVED')
    print('PHASE177_R14_ACTUAL_ROOT_COMPLETION=NOT_CLAIMED')
