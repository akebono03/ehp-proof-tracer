"""Phase 172 R4: canonical proof, retained citations and safe suppression."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_26_exactness_projection import project_exactness_chains
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r2_suspension_relation_display.projection import redundant_suspension_relation_indices
from phase172_r3_hopf_chain_display.projection import project_verified_hopf_chain
from phase172_r4_hopf_surjectivity_display.projection import redundant_hopf_surjectivity_indices
from proof import ProofRule
from toda_rules import TodaHopfInvariantSurjectiveStatement


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
    chains = project_exactness_chains(model)
    suppressed = {index for chain in chains for index in chain.step_indices}
    order = tuple(
        item.step_index
        for item in project_narrative_order(model, suppressed)
        if item.step_index in scope
    )
    suppressed.update(redundant_suspension_relation_indices(model, order, suppressed))
    hopf = project_verified_hopf_chain(model, order, suppressed)
    assert hopf is not None
    suppressed.update(hopf.hidden_indices)
    return result, model, order, suppressed


def _repetition(model, hidden):
    assert len(hidden) == 1
    later_index = next(iter(hidden))
    later = model.steps[later_index]
    assert isinstance(later.conclusion, MapSurjective)
    delta = next(step for step in later.premises if type(step.conclusion).__name__ == "TodaDeltaZeroStatement")
    earlier = next(step for step in delta.premises if isinstance(step.conclusion, TodaHopfInvariantSurjectiveStatement))
    earlier_index = next(i for i, step in enumerate(model.steps) if step is earlier)
    return earlier_index, later_index


def test_real_completed_proof_hides_only_later_h_surjectivity(verified_pi63):
    result, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    earlier_index, later_index = _repetition(model, hidden)
    assert earlier_index not in hidden
    assert earlier_index in order and later_index in order
    assert model.steps[earlier_index].conclusion.map == model.steps[later_index].conclusion.map
    assert model.steps[earlier_index].rule is ProofRule.INFERENCE
    assert model.steps[later_index].rule is ProofRule.INFERENCE
    assert not model.step_citation_numbers[later_index]
    assert result.proven_steps == model.steps
    assert len(model.citations) == 8


def test_real_web_prose_retains_first_h_and_short_exact_sequence(verified_pi63):
    result, model, order, suppressed = verified_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    assert "[R6] Proposition 4.2 (4.4)." in references
    assert r"$H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射." in body
    assert r"完全性より, $H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射." not in body
    assert r"$H$ の全射性と完全性より" in body
    assert r"0\longrightarrow \pi_{5}^{2}" in body
    assert r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}" in body
    assert r"H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}" in body
    assert len(model.citations) == 8


def test_direct_citation_on_later_statement_preserves_later_line(verified_pi63):
    _, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    _, later = _repetition(model, hidden)
    updated = list(model.step_citation_numbers)
    updated[later] = (6,)
    changed = replace(model, step_citation_numbers=tuple(updated))
    assert redundant_hopf_surjectivity_indices(changed, order, suppressed) == frozenset()


def test_hidden_earlier_source_prevents_suppression(verified_pi63):
    _, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    earlier, later = _repetition(model, hidden)
    assert redundant_hopf_surjectivity_indices(
        model, order, set(suppressed).union({earlier}),
    ) == frozenset()
    assert redundant_hopf_surjectivity_indices(
        model, tuple(i for i in order if i != earlier), suppressed,
    ) == frozenset()
    assert later not in suppressed


def test_incomplete_or_invalid_root_never_suppresses(verified_pi63):
    _, model, order, suppressed = verified_pi63
    for changed in (
        replace(model, status=ProofSearchStatus.PARTIAL),
        replace(model, open_goals=("unresolved",)),
        replace(model, root_index=None),
    ):
        assert redundant_hopf_surjectivity_indices(changed, order, suppressed) == frozenset()
    assert redundant_hopf_surjectivity_indices(model, order + (order[0],), suppressed) == frozenset()


def test_missing_source_citation_or_different_map_preserves_both(verified_pi63):
    _, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    earlier, later = _repetition(model, hidden)
    cited = list(model.step_citation_numbers)
    for i in root_ancestor_step_indices(model.steps, earlier):
        if model.steps[i].rule is ProofRule.GIVEN:
            cited[i] = ()
    changed = replace(model, step_citation_numbers=tuple(cited))
    assert redundant_hopf_surjectivity_indices(changed, order, suppressed) == frozenset()
    alternate = replace(model.steps[later].conclusion, map=object())
    modified_steps = list(model.steps)
    modified_steps[later] = replace(model.steps[later], conclusion=alternate)
    modified_model = replace(model, steps=tuple(modified_steps))
    assert redundant_hopf_surjectivity_indices(modified_model, order, suppressed) == frozenset()
