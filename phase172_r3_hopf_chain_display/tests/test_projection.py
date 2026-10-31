"""Live canonical proof tests and fail-closed Hopf narration checks."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase168_r3_26_exactness_projection import project_exactness_chains
from phase168_r3_29_order_projection import project_narrative_order
from phase172_r2_suspension_relation_display.projection import redundant_suspension_relation_indices
from phase172_r3_hopf_chain_display.projection import project_verified_hopf_chain
from proof import ProofRule


@pytest.fixture(scope="module")
def verified_pi63():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    chains = tuple(
        chain for chain in project_exactness_chains(model)
        if all(i in scope for i in chain.step_indices)
    )
    suppressed = {i for chain in chains for i in chain.step_indices}
    order = tuple(
        entry.step_index
        for entry in project_narrative_order(model, suppressed)
        if entry.step_index in scope
    )
    r2_hidden = redundant_suspension_relation_indices(model, order, suppressed)
    assert len(r2_hidden) == 2
    return result, model, order, set(suppressed).union(r2_hidden)


def test_real_hopf_chain_preserves_verified_citations_and_premises(verified_pi63):
    result, model, order, hidden = verified_pi63
    display = project_verified_hopf_chain(model, order, hidden)
    assert display is not None
    assert len(display.hidden_indices) == 5
    assert display.hidden_indices.isdisjoint(hidden)
    assert display.formula_index not in display.hidden_indices
    assert display.image_index not in display.hidden_indices
    assert display.formula_citations
    assert len(display.image_citations) == 3
    assert set(display.formula_citations).issubset(display.image_citations)
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in display.hidden_indices)
    assert all(not model.step_citation_numbers[i] for i in display.hidden_indices)
    assert result.proven_steps == model.steps
    assert len(model.citations) == 8


def test_real_public_narrative_shortens_hopf_chain_only(verified_pi63):
    result, model, order, hidden = verified_pi63
    display = project_verified_hopf_chain(model, order, hidden)
    assert display is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    assert "[R3] Chapter V, i)." in reference
    assert "[R4] Proposition 2.2." in reference
    assert "[R5] (5.3)." in reference
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert r"$E\eta_{5} = \eta_{6}$." not in body
    assert r"$\eta_{6} = E\eta_{5}$." not in body
    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." not in body
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert "[R4]より, " in body
    assert "[R3], [R4], [R5]より, " in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}" in body
    assert len(model.citations) == 8


def test_missing_reference_prevents_hopf_shortening(verified_pi63):
    _, model, order, hidden = verified_pi63
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    reference_source = model.steps[verified.formula_index].premises[0]
    source_index = next(i for i, step in enumerate(model.steps) if step is reference_source)
    changed = list(model.step_citation_numbers)
    changed[source_index] = ()
    assert project_verified_hopf_chain(
        replace(model, step_citation_numbers=tuple(changed)), order, hidden,
    ) is None


def test_hidden_source_or_missing_r2_guards_prevents_shortening(verified_pi63):
    _, model, order, hidden = verified_pi63
    assert project_verified_hopf_chain(model, order, set()) is None
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    assert project_verified_hopf_chain(
        replace(model, root_index=None), order, hidden,
    ) is None
    assert project_verified_hopf_chain(
        replace(model, status=ProofSearchStatus.PARTIAL), order, hidden,
    ) is None
    assert project_verified_hopf_chain(
        replace(model, open_goals=("unresolved",)), order, hidden,
    ) is None


def test_direct_citation_on_intermediate_prevents_shortening(verified_pi63):
    _, model, order, hidden = verified_pi63
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    changed = list(model.step_citation_numbers)
    selected = next(iter(verified.hidden_indices))
    changed[selected] = verified.formula_citations
    assert project_verified_hopf_chain(
        replace(model, step_citation_numbers=tuple(changed)), order, hidden,
    ) is None


def test_unrelated_or_invalid_display_order_is_unchanged(verified_pi63):
    _, model, order, hidden = verified_pi63
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    assert project_verified_hopf_chain(model, order + (order[0],), hidden) is None
    assert project_verified_hopf_chain(
        model, tuple(i for i in order if i != verified.formula_index), hidden,
    ) is None
