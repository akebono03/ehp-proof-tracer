"""Phase 172 R5: reference headings keep every original proof provenance."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r5_prior_reference_display.projection import (
    display_prior_reference_locator,
)
from proof import LiteratureReference


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
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    assert len(model.citations) == 8
    return result, model


def test_verified_prior_headings_identify_typed_groups_and_metadata(verified_pi63):
    result, model = verified_pi63
    headers = [display_prior_reference_locator(c, model) for c in model.citations]
    assert [i + 1 for i, value in enumerate(headers) if value is not None] == [2, 8]
    assert headers[1] == (
        r"先行データベース結果 $\pi_{7}^{5}$"
        "（sphere.csv, n=5, k=2）［参考: Proposition 5.3］"
    )
    assert headers[7] == (
        r"先行データベース結果 $\pi_{6}^{5}$"
        "（sphere.csv, n=5, k=1）［参考: Proposition 5.1］"
    )
    assert result.proven_steps == model.steps


def test_public_reference_headings_change_without_rewriting_source(verified_pi63):
    result, model = verified_pi63
    before_locators = tuple(c.reference.locator for c in model.citations)
    before_numbers = model.step_citation_numbers
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    assert "DB prior: sphere.csv" not in reference
    assert "[R2] 先行データベース結果" in reference
    assert "[R8] 先行データベース結果" in reference
    assert "[R3] Chapter V, i)." in reference
    assert "[R4] Proposition 2.2." in reference
    assert "[R5] (5.3)." in reference
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert len(model.steps) == 50
    assert len(model.citations) == 8
    assert tuple(c.reference.locator for c in model.citations) == before_locators
    assert model.step_citation_numbers == before_numbers
    assert model.open_goals == ()


def test_unrelated_literature_reference_keeps_original_locator(verified_pi63):
    _, model = verified_pi63
    for citation in model.citations:
        if citation.number not in (2, 8):
            assert display_prior_reference_locator(citation, model) is None


def test_forged_prior_marker_is_not_presented_as_database(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[1]
    index = citation.step_indices[0]
    changed_steps = list(model.steps)
    changed_steps[index] = replace(changed_steps[index], note="unverified")
    altered = replace(model, steps=tuple(changed_steps))
    assert display_prior_reference_locator(citation, altered) is None


def test_mismatched_coordinates_or_locator_fail_closed(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[1]
    forged = replace(
        citation,
        reference=LiteratureReference(
            label="DB prior: sphere.csv (n=8, k=2)",
            locator="DB prior: sphere.csv (n=8, k=2)",
        ),
    )
    assert display_prior_reference_locator(forged, model) is None
    assert display_prior_reference_locator(
        replace(citation, step_indices=()), model,
    ) is None
    assert display_prior_reference_locator(
        replace(citation, assertion_ids=("invented",)), model,
    ) is None


def test_missing_reference_ownership_and_incomplete_model_fail_closed(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[1]
    index = citation.step_indices[0]
    numbers = list(model.step_citation_numbers)
    numbers[index] = ()
    assert display_prior_reference_locator(
        citation, replace(model, step_citation_numbers=tuple(numbers)),
    ) is None
    assert display_prior_reference_locator(
        citation, replace(model, status=ProofSearchStatus.PARTIAL),
    ) is None
    assert display_prior_reference_locator(
        citation, replace(model, open_goals=("pending",)),
    ) is None


def test_no_prior_without_real_step_or_root(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[7]
    assert display_prior_reference_locator(
        citation, replace(model, root_index=None),
    ) is None
    assert display_prior_reference_locator(
        citation, replace(model, steps=()),
    ) is None
