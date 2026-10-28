"""R10ET-R5 focused production-path tests: no in-memory provider override."""
from __future__ import annotations

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
from phase169_r10et_r4_cyclic_definition_projection.policy import (
    canonical_definition_image,
)
from phase165_r14_r6_generic_iso import GeneratorImage


@pytest.fixture(scope="module")
def production_cases():
    bridge = build_shared_typed_bridge()
    output = {}
    for n, k in ((22, 6), (30, 9), (43, 26), (4, 2)):
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        assert result.status is ProofSearchStatus.COMPLETE
        assert not result.open_goals and len(contexts) == 1
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        verify_proof_tree_for_narrative(
            result, contexts[0], citing_assertion_id=citing,
            derived_target_without_citing_id=citing is None,
        )
        model = build_linked_proof_narrative_model(result, contexts[0])
        order = tuple(item.step_index for item in project_narrative_order(model))
        output[(n, k)] = result, model, order
    return output


def test_r5_live_cyclic_proof_no_longer_needs_family_definition(production_cases):
    result, model, order = production_cases[(22, 6)]
    display = project_verified_stable_image_chain(model, order)
    assert display is not None
    assert display.citation_numbers == ()
    images = model.steps[model.root_index].premises[2:]
    assert images and all(canonical_definition_image(step) for step in images)
    text = render_model_backed_narrative_markdown(result, model)
    assert "Definition より, $E^{14}" in text
    assert text.rstrip().endswith("□")
    refs = tuple(item.reference.locator or item.reference.label
                 for item in model.citations)
    assert len(refs) == 2 and refs[0].startswith("DB prior:") and refs[1] == "(4.5)"


def test_r5_live_direct_sum_proof_uses_only_common_definition(production_cases):
    for key in ((30, 9), (43, 26)):
        result, model, order = production_cases[key]
        display = project_verified_direct_sum_transport(model, order)
        assert display is not None
        assert display.statement.startswith("Definition より, ")
        assert display.statement in render_model_backed_narrative_markdown(result, model)
        images = [step for step in model.steps
                  if isinstance(step.conclusion, GeneratorImage)]
        assert images and all(canonical_definition_image(step) for step in images)
        refs = tuple(item.reference.locator or item.reference.label
                     for item in model.citations)
        assert len(refs) == 2 and refs[0].startswith("DB prior:") and refs[1] == "(4.5)"


def test_r5_live_low_stem_remains_complete(production_cases):
    result, model, _ = production_cases[(4, 2)]
    assert result.status is ProofSearchStatus.COMPLETE
    assert not any(canonical_definition_image(step) for step in model.steps)
    assert render_model_backed_narrative_markdown(result, model).rstrip().endswith("□")
