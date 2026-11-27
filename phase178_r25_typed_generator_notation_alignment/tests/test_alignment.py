from dataclasses import replace

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple, Zero
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase166_r3af_goal_adapter import _generator_for_target
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_prior_group_step, exact_prior_database_result, verified_db_step,
)
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase178_r16_toda513_isolated.source import canonical_513, build_cited_513_source
from phase178_r21_finite_cyclic_generator_zero_image_isolated import rule as r21
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule
from toda_rules import TodaDeltaImageUpToSignStatement, TodaDeltaZeroStatement


def test_only_single_eta_notation_changed():
    def element(family,n,k):
        name = family+str(n).translate(str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉'))
        return HomotopyElement(name,n,n+k,n,GeneratorSymbol(family,index=n))
    signed, z11, z13 = canonical_513()
    assert signed == TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(12,9),TodaPrimaryGroup(10,4)),
        element('ν',9,3),Multiple(2,Composition(element('ν',4,3),element('ν',7,3))))
    assert z11 == GeneratorImage(TodaDeltaMap(TodaPrimaryGroup(13,11),TodaPrimaryGroup(11,5)),
        Composition(element('η',11,1),element('η',12,1)),Zero())
    eta = _generator_for_target('η13',13,13,1)
    assert eta == HomotopyElement('η_13',13,14,13,GeneratorSymbol('η',index=13))
    assert z13 == GeneratorImage(TodaDeltaMap(TodaPrimaryGroup(14,13),TodaPrimaryGroup(12,6)),eta,Zero())
    assert eta != element('η',13,1)
    domain = exact_prior_database_result(13,1)
    assert domain.rhs.order==2 and domain.rhs.generator==eta
    bridge = build_cited_513_source()
    assert tuple(link.step.conclusion for link in bridge.proof_links)==(signed,z11,z13)
    assert len(bridge.registry._assertions)==3
    assert all(link.step.rule is ProofRule.GIVEN and not link.step.premises for link in bridge.proof_links)
    print('PHASE178_R25_OTHER_513_CLAIMS_UNCHANGED=VERIFIED')


def test_real_n7_cited_zero_image_replays_without_relaxation():
    root = exact_prior_database_result(7,6)
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root)
    image = canonical_513()[2]
    goal = TodaDeltaZeroStatement(image.map)
    prior = admitted_prior_group_step(image.map.source_group,proof_target=root,bridge=bridge)
    assert prior is not None and verified_db_step(prior,proof_target=root,bridge=bridge)
    assert prior.conclusion==exact_prior_database_result(13,1)
    cited, = linked_cited_steps(bridge,image)
    assert cited.inference_rule.literature_reference.locator=='(5.13)'
    required = (prior.conclusion,cited.conclusion)
    option, = [o for o in r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)(goal)
               if o.rule.name==r21.RULE_NAME and o.subgoals==required]
    match, = find_inference_matches_for_rule(option.rule,(prior,cited))
    proved = apply_inference_match(match)
    assert proved.conclusion==goal and proved.rule is ProofRule.INFERENCE and proved.premises==(prior,cited)
    assert sum(o.rule.name==r21.RULE_NAME and o.subgoals==required
               for o in shared_expansion_provider(bridge,proof_target=root)(goal))==1
    assert not any(link.step is not None and link.step.conclusion==root for link in bridge.proof_links)
    old_image = replace(image,source_generator=replace(image.source_generator,name='η₁₃'))
    wrong = replace(cited,conclusion=old_image)
    for parents in ((prior,wrong),(prior,ProofStep(image,(),ProofRule.GIVEN)),(prior,)):
        assert not find_inference_matches_for_rule(option.rule,parents)
    missing = replace(bridge,proof_links=tuple(link for link in bridge.proof_links if link.step!=cited))
    assert not r21.build_finite_cyclic_delta_zero_provider(bridge=missing,proof_target=root)(goal)
    print('PHASE178_R25_N7_DELTA_ZERO_REPLAY=VERIFIED')
