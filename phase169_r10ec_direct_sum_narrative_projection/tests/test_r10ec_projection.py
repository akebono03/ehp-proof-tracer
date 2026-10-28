"""R10EC proof-preserving compression tests on the real screened search."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import FiniteCyclicGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from proof import ProofRule, ProofStep, Relation


@pytest.fixture(scope="module")
def pi39():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=30, k=9, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is None
    assert isinstance(result.conclusion, Relation)
    verify_proof_tree_for_narrative(
        result, contexts[-1], citing_assertion_id=None,
        derived_target_without_citing_id=True,
    )
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    return result, model, order


def test_r10ec_complete_pi39_compresses_all_verified_image_prose(pi39):
    result, model, order = pi39
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    assert display.root_index == model.root_index
    assert display.hidden_indices
    assert model.root_index not in display.hidden_indices
    assert len(display.citation_numbers) >= 3
    assert r"E^{19}(\nu_{11}^{3})=\nu_{30}^{3}" in display.statement
    assert r"E^{19}(\mu_{11})=\mu_{30}" in display.statement
    assert r"E^{19}(\eta_{11}\varepsilon_{12})=\eta_{30}\varepsilon_{31}" in display.statement
    markdown = render_model_backed_narrative_markdown(result, model)
    assert display.statement in markdown
    assert count_rendered_image_equations(markdown)["extra_duplicate_occurrences"] == 0
    assert len(markdown) < 4167
    for citation in model.citations:
        label = citation.reference.locator or citation.reference.label
        assert f"**[R{citation.number}] {label}.**" in markdown
    assert markdown.rstrip().endswith("□")


def test_r10ec_refuses_uncited_source_and_invalid_model(pi39):
    _, model, order = pi39
    uncited = replace(
        model, step_citation_numbers=tuple(() for _ in model.steps),
        citations=(),
    )
    assert project_verified_direct_sum_transport(uncited, order) is None
    assert project_verified_direct_sum_transport(replace(model, root_index=None), order) is None
    assert project_verified_direct_sum_transport(model, order + (order[0],)) is None


def test_r10ec_never_hides_image_used_by_an_external_proof_step(pi39):
    _, model, order = pi39
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    candidate = model.steps[display.hidden_indices[0]]
    # An independent consumer outside the transport proof prevents compression.
    external = ProofStep(candidate.conclusion, (candidate,), ProofRule.INFERENCE)
    modified = replace(
        model,
        steps=model.steps + (external,),
        step_citation_numbers=model.step_citation_numbers + ((),),
    )
    assert project_verified_direct_sum_transport(
        modified, order + (len(model.steps),),
    ) is None


def test_r10ec_cyclic_non_direct_sum_is_not_compressed():
    """Use the already verified complete cyclic pi_10^8 fixture from R10A."""
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=8, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    assert isinstance(result.conclusion, Relation)
    assert isinstance(result.conclusion.rhs, FiniteCyclicGroup)
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    assert project_verified_direct_sum_transport(model, order) is None
