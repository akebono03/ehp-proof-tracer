"""R10A focused test: typed, cited, complete image-chain compression."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def pi108():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=8, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == () and len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_r10a_4fold_eta_square_is_single_certified_display(pi108):
    result, model = pi108
    order = tuple(range(len(model.steps)))
    display = project_verified_stable_image_chain(model, order)
    assert display is not None
    assert display.exponent == 4
    assert display.root_index == model.root_index
    assert len(display.hidden_indices) >= 4
    assert display.citation_numbers
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in display.hidden_indices)
    original_length = len(model.steps)
    narrative = render_model_backed_narrative_markdown(result, model)
    assert len(model.steps) == original_length
    assert "E^{4}" in narrative
    assert "\\eta_{8}" in narrative
    # The Toda (4.5) isomorphism and the generator equality BOTH use E^4.
    # Count only the exact generator equation, not the common prefix.
    assert narrative.count(r"$E^{4}(\eta_{4}^{2})=\eta_{8}^{2}$") == 1
    assert narrative.count("$E^{4}:") == 1
    assert "E(\\eta_{5})" not in narrative
    assert "E(\\eta_{6})" not in narrative
    assert narrative.rstrip().endswith("□")


def test_r10a_partial_or_unrelated_model_cannot_be_compressed(pi108):
    _, model = pi108
    assert project_verified_stable_image_chain(model, ()) is None
    modified = replace(model, root_index=None)
    assert project_verified_stable_image_chain(modified, tuple(range(len(model.steps)))) is None


def test_r10a_web_and_existing_2stem_complete(pi108):
    result, model = pi108
    view = build_standard_web_group_proof_view(8, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert len(view.steps) == len(result.proven_steps)
    for n in (5, 6, 7):
        other = build_standard_web_group_proof_view(n, 2, mode="narrative")
        assert other.key == "generic-complete-proof"
        assert not other.partial_result


def test_r10a_patch_guard_and_full_function_export():
    from phase169_r10a_verified_stable_chain_projection.patch import (
        EXPECTED_SHA256, NEW, OLD, replacement_content,
    )
    assert "project_verified_stable_image_chain" in NEW
    assert "for index in order" in OLD
    with pytest.raises(RuntimeError, match="SHA256 differs"):
        replacement_content(b"invalid bytes", expected_sha256=EXPECTED_SHA256)
