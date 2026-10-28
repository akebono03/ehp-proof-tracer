"""Focused R10ET-R4 regression: trusted real proofs, both legacy and Definition."""
from __future__ import annotations

import re
from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10et_r2_shadow_common_definition_comparison.audit import (
    shadow_provider_factory,
)
from phase169_r10et_r4_cyclic_definition_projection.policy import (
    canonical_definition_image,
    verified_cyclic_generator_image_citation_numbers,
)
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule


@pytest.fixture(scope="module")
def shadow_cases():
    import phase165_r52_r9_shared_math as shared

    bridge = build_shared_typed_bridge()
    original = shared.shared_expansion_provider
    cases = {}
    try:
        shared.shared_expansion_provider = shadow_provider_factory(original)
        for n, k in ((22, 6), (22, 10), (15, 8), (24, 9), (43, 26)):
            contexts = []
            result = search_group_from_registered_goal(
                n=n, k=k, bridge=bridge, context_sink=contexts.append,
            )
            assert result.status is ProofSearchStatus.COMPLETE
            assert result.open_goals == () and len(contexts) == 1
            citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
            verify_proof_tree_for_narrative(
                result, contexts[0], citing_assertion_id=citing,
                derived_target_without_citing_id=citing is None,
            )
            model = build_linked_proof_narrative_model(result, contexts[0])
            order = tuple(row.step_index for row in project_narrative_order(model))
            cases[(n, k)] = result, model, order
    finally:
        shared.shared_expansion_provider = original
    return cases


@pytest.mark.parametrize(("n", "k", "exponent"), ((22, 6, 14), (22, 10, 10)))
def test_r10et_r4_cyclic_shadow_definition_is_compressed_and_labelled(
    shadow_cases, n, k, exponent,
):
    result, model, order = shadow_cases[(n, k)]
    before = (tuple(map(id, model.steps)), model.step_citation_numbers)
    display = project_verified_stable_image_chain(model, order)
    assert display is not None
    assert display.exponent == exponent
    assert display.citation_numbers == ()
    assert display.hidden_indices
    text = render_model_backed_narrative_markdown(result, model)
    assert f"Definition より, $E^{{{exponent}}}" in text
    assert re.search(r"(?m)^より, \$E\^", text) is None
    assert text.rstrip().endswith("□")
    assert (tuple(map(id, model.steps)), model.step_citation_numbers) == before
    locators = tuple(row.reference.locator or row.reference.label
                     for row in model.citations)
    assert any("DB prior:" in locator for locator in locators)
    assert "(4.5)" in locators
    assert all("family definition" not in locator for locator in locators)


@pytest.mark.parametrize(("n", "k"), ((15, 8), (24, 9), (43, 26)))
def test_r10et_r4_direct_sum_shadow_keeps_existing_projection(shadow_cases, n, k):
    result, model, order = shadow_cases[(n, k)]
    before = (tuple(map(id, model.steps)), model.step_citation_numbers)
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    text = render_model_backed_narrative_markdown(result, model)
    assert display.statement in text
    assert text.rstrip().endswith("□")
    assert (tuple(map(id, model.steps)), model.step_citation_numbers) == before


def test_r10et_r4_rejects_missing_root_citation_even_with_valid_images(shadow_cases):
    _, model, order = shadow_cases[(22, 6)]
    good = project_verified_stable_image_chain(model, order)
    assert good is not None
    root = model.steps[model.root_index]
    source = root.premises[0]
    index = next(i for i, step in enumerate(model.steps) if step is source)
    bad_links = list(model.step_citation_numbers)
    assert bad_links[index]
    bad_links[index] = ()
    invalid = replace(model, step_citation_numbers=tuple(bad_links))
    assert project_verified_stable_image_chain(invalid, order) is None
    assert project_verified_stable_image_chain(replace(model, root_index=None), order) is None


def test_r10et_r4_definition_must_be_canonical_inference(shadow_cases):
    _, model, order = shadow_cases[(22, 6)]
    root = model.steps[model.root_index]
    images = root.premises[2:]
    assert images
    assert all(isinstance(step.conclusion, GeneratorImage) for step in images)
    assert all(canonical_definition_image(step) for step in images)
    assert verified_cyclic_generator_image_citation_numbers(model, order, images) == ()
    first = images[0]
    counterfeit = replace(
        first, inference_rule=replace(first.inference_rule, name="counterfeit name"),
    )
    assert not canonical_definition_image(counterfeit)
    assert not canonical_definition_image(
        replace(first, rule=ProofRule.GIVEN),
    )
    assert not canonical_definition_image(
        replace(first, premises=(first,)),
    )
