"""Real searched complete-proof and display regressions after R10EL consolidation."""
from __future__ import annotations

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
from phase169_r10el_shared_generator_suppression.core import (
    exclusive_generator_inference_indices,
)
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from proof import ProofRule, ProofStep, Relation


CASES = (
    (22, 6, "cyclic", 14, 14),
    (22, 10, "cyclic", 10, 10),
    (15, 8, "direct_sum", 5, 10),
    (24, 9, "direct_sum", 13, 39),
)


@pytest.fixture(scope="module", params=CASES)
def verified_case(request):
    n, k, shape, exponent, hidden_count = request.param
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals and contexts
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None or (
        isinstance(result.conclusion, Relation)
        and result.conclusion.lhs == result.target
    )
    verify_proof_tree_for_narrative(
        result, contexts[-1], citing_assertion_id=citing_id,
        derived_target_without_citing_id=citing_id is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(item.step_index for item in project_narrative_order(model))
    return result, model, order, shape, exponent, hidden_count


def _display(model, order, shape):
    return (project_verified_stable_image_chain(model, order)
            if shape == "cyclic"
            else project_verified_direct_sum_transport(model, order))


def test_r10el_shared_contract_matches_existing_projection(verified_case):
    result, model, order, shape, exponent, count = verified_case
    display = _display(model, order, shape)
    assert display is not None
    assert len(display.hidden_indices) == count
    root = model.steps[model.root_index]
    _, _, *images = root.premises
    shared = exclusive_generator_inference_indices(
        model, order, images, model.root_index,
        require_all=shape == "direct_sum",
    )
    assert shared is not None
    assert shared == display.hidden_indices
    assert model.steps == result.proven_steps
    assert all(model.steps[i].rule is ProofRule.INFERENCE
               and not model.step_citation_numbers[i]
               for i in display.hidden_indices)


def test_r10el_preserves_complete_narrative_and_references(verified_case):
    result, model, order, shape, exponent, count = verified_case
    display = _display(model, order, shape)
    assert display is not None
    text = render_model_backed_narrative_markdown(result, model)
    assert text.rstrip().endswith("□")
    assert count_rendered_image_equations(text)["extra_duplicate_occurrences"] == 0
    assert count_rendered_image_equations(text)["total_occurrences"] == 0
    assert rf"E^{{{exponent}}}" in text
    for citation in model.citations:
        assert f"**[R{citation.number}] " in text
    assert set(display.citation_numbers).issubset({x.number for x in model.citations})


def test_r10el_external_consumer_refuses_or_retains_prose(verified_case):
    _, model, order, shape, _, _ = verified_case
    original = _display(model, order, shape)
    assert original is not None
    candidate_index = original.hidden_indices[0]
    candidate = model.steps[candidate_index]
    extra = ProofStep(candidate.conclusion, (candidate,), ProofRule.INFERENCE)
    modified = replace(
        model,
        steps=model.steps + (extra,),
        step_citation_numbers=model.step_citation_numbers + ((),),
    )
    changed = _display(modified, order + (len(model.steps),), shape)
    if shape == "direct_sum":
        assert changed is None
    else:
        assert changed is None or candidate_index not in changed.hidden_indices


def test_r10el_citations_are_never_suppressed(verified_case):
    _, model, order, shape, _, _ = verified_case
    original = _display(model, order, shape)
    assert original is not None
    target = original.hidden_indices[0]
    links = list(model.step_citation_numbers)
    links[target] = (model.citations[0].number,)
    modified = replace(model, step_citation_numbers=tuple(links))
    changed = _display(modified, order, shape)
    assert changed is None or target not in changed.hidden_indices
