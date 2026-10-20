"""Focused tests: one source Hopf image, typed derivation, safety and regressions."""
from dataclasses import replace

from expression import HomotopyElement
from phase165_r14_r33_final_group import hopf_eta2_image_step
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase166_r3q_hopf_image_relation import expand_hopf_image_relation
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def test_single_hopf_source_is_direct_given():
    bridge = build_shared_typed_bridge()
    image_id = "shared:1:adopted:assertion:5"
    assert bridge.registry.assertion(image_id).component_position == 100
    image_links = [link for link in bridge.proof_links if link.assertion_id == image_id]
    assert len(image_links) == 1
    assert image_links[0].step.rule is ProofRule.GIVEN
    for key in (
        "shared:2:toda:adopted:prop5.1:eta2_hopf_relation",
        "shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation",
    ):
        assert bridge.registry.assertion(key).component_position == 100
        assert not any(link.assertion_id == key for link in bridge.proof_links)


def test_relation_follows_by_inference_from_hopf_image():
    bridge = build_shared_typed_bridge()
    goal = bridge.registry.assertion("shared:2:toda:adopted:prop5.1:eta2_hopf_relation").content
    image = hopf_eta2_image_step().conclusion
    options = expand_hopf_image_relation(goal, (image,))
    assert len(options) == 1
    assert options[0].subgoals == (image,)
    matches = find_inference_matches_for_rule(
        options[0].rule, (ProofStep(conclusion=image, premises=(), rule=ProofRule.GIVEN),)
    )
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert len(derived.premises) == 1
    assert derived.premises[0].conclusion == image


def test_hopf_relation_rejects_wrong_generator():
    bridge = build_shared_typed_bridge()
    goal = bridge.registry.assertion("shared:2:toda:adopted:prop5.1:eta2_hopf_relation").content
    image = hopf_eta2_image_step().conclusion
    wrong = replace(image, target_generator=replace(image.target_generator, generator=None))
    assert expand_hopf_image_relation(goal, (wrong,)) == ()


def test_shared_expansion_proposes_derived_relation():
    bridge = build_shared_typed_bridge()
    goal = bridge.registry.assertion("shared:2:toda:adopted:prop5.1:eta2_hopf_relation").content
    options = shared_expansion_provider(bridge)(goal)
    assert any(option.subgoals == (hopf_eta2_image_step().conclusion,) for option in options)
