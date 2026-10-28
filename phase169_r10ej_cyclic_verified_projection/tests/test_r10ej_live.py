"""Live certified cyclic projection and citation-preserving guard regressions."""
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
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from proof import Relation


@pytest.fixture(scope="module", params=((22, 6, 14), (22, 10, 10)))
def proven_cyclic_case(request):
    n, k, exponent = request.param
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    derived = citing is None
    assert not derived or (isinstance(result.conclusion, Relation)
                           and result.conclusion.lhs == result.target)
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=derived,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(item.step_index for item in project_narrative_order(model))
    return result, model, order, exponent


def test_r10ej_replaces_proved_nested_images_by_one_aggregate(proven_cyclic_case):
    result, model, order, exponent = proven_cyclic_case
    display = project_verified_stable_image_chain(model, order)
    assert display is not None
    assert display.exponent == exponent
    assert len(display.hidden_indices) > exponent
    original_steps = result.proven_steps
    narrative = render_model_backed_narrative_markdown(result, model)
    assert result.proven_steps == original_steps == model.steps
    assert narrative.count(
        f"$E^{{{exponent}}}({display.source_tex})={display.target_tex}$"
    ) == 1
    assert count_rendered_image_equations(narrative)["total_occurrences"] == 0
    for citation in model.citations:
        assert f"**[R{citation.number}] " in narrative


def test_r10ej_incomplete_or_missing_root_cannot_be_projected(proven_cyclic_case):
    _, model, order, _ = proven_cyclic_case
    assert project_verified_stable_image_chain(model, ()) is None
    assert project_verified_stable_image_chain(replace(model, root_index=None), order) is None


def test_r10ej_ancestor_with_own_citation_is_never_suppressed(proven_cyclic_case):
    _, model, order, _ = proven_cyclic_case
    original = project_verified_stable_image_chain(model, order)
    assert original is not None
    nested = next(index for index in original.hidden_indices
                  if index not in {next(i for i, step in enumerate(model.steps)
                                   if step is p)
                                   for p in model.steps[model.root_index].premises[2:]})
    cited = list(model.step_citation_numbers)
    cited[nested] = (model.citations[0].number,)
    altered = replace(model, step_citation_numbers=tuple(cited))
    projected = project_verified_stable_image_chain(altered, order)
    assert projected is not None
    assert nested not in projected.hidden_indices
