"""Focused R4R14R9 literature-provenance and inferred-zero tests."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r14r9_literature_zero_image.rule import (
    RULE_NAME, verified_literature_zero_image_inputs, literature_zero_image_rule,
)
from phase175_r4r14r9_literature_zero_image.provider import build_literature_zero_image_provider
from proof import InferenceRule, ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def _case():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    presentation = exact_prior_database_result(5, 4)
    assert presentation is not None
    mapping = TodaSuspensionMap(presentation.lhs, root.group)
    goal = ImageZeroStatement(mapping)
    zero = GeneratorImage(mapping, presentation.rhs.generator, Zero())
    return root, bridge, presentation, goal, zero


def test_literature_link_and_generator_zero_prove_image_zero():
    root, bridge, presentation, goal, zero = _case()
    verified = verified_literature_zero_image_inputs(
        goal, presentation, proof_target=root, bridge=bridge,
    )
    assert verified is not None
    obligations, cited_step = verified
    assert obligations == (presentation, zero)
    assert cited_step.rule is ProofRule.GIVEN
    assert any(link.step == cited_step for link in bridge.proof_links)
    separate = ProofStep(zero, (), ProofRule.INFERENCE,
                         inference_rule=InferenceRule(name="test independently inferred E(g)=0"))
    rule = literature_zero_image_rule(goal, presentation, proof_target=root, bridge=bridge)
    matches = find_inference_matches_for_rule(rule, (cited_step, separate))
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal
    assert find_inference_matches_for_rule(rule, (replace(cited_step, note="forged note"), separate)) == ()
    assert find_inference_matches_for_rule(rule, (replace(cited_step, inference_rule=None), separate)) == ()
    assert find_inference_matches_for_rule(rule, (cited_step, replace(separate, rule=ProofRule.GIVEN))) == ()


def test_public_provider_proposes_without_adding_given():
    root, bridge, presentation, goal, zero = _case()
    before = tuple(bridge.proof_links)
    proposals = build_literature_zero_image_provider(
        bridge=bridge, proof_target=root,
    )(goal)
    assert len(proposals) == 1
    assert proposals[0].rule.name == RULE_NAME
    assert proposals[0].subgoals == (presentation, zero)
    assert all(not isinstance(x, ProofStep) for x in proposals[0].subgoals)
    assert bridge.proof_links == before
    shared = shared_expansion_provider(bridge, proof_target=root)(goal)
    assert any(x.rule.name == RULE_NAME for x in shared)


def test_missing_citation_and_same_group_root_fail_closed():
    root, bridge, presentation, goal, zero = _case()
    empty = RegistryBridgeResult(bridge.registry, bridge.records, ())
    assert build_literature_zero_image_provider(bridge=empty, proof_target=root)(goal) == ()
    assert verified_literature_zero_image_inputs(
        goal, presentation, proof_target=TodaPrimaryGroupZeroStatement(presentation.lhs),
        bridge=bridge,
    ) is None
