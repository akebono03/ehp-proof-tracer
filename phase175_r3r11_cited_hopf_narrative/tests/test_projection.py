"""End-to-end cited Proof Tree narration; no database-given group conclusions."""
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
from phase175_r3r11_cited_hopf_narrative.projection import (
    project_verified_source_and_hopf_summary,
)


@pytest.fixture(scope="module")
def pi73_verified():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=4, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    cited = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=cited)
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_references_and_zero_composition_are_explicit(pi73_verified) -> None:
    result, model = pi73_verified
    content = render_model_backed_narrative_markdown(result, model)
    reference, body = content.split("\n証明\n", 1)
    assert "**[R2] Lemma 5.7.**" in reference
    assert r"$E(\eta_2\nu')=0$." in reference
    assert "**[R6] Proposition 2.2.**" in reference
    assert r"$H(\alpha E\beta)=H(\alpha) E\beta$." in reference
    assert r"[R2]より, $E(\eta_{2}\nu')=0$." in body
    assert r"$E(\eta_{2}\circ " not in body
    assert len(model.citations) == 7


def test_hopf_chain_is_source_bound_and_compact(pi73_verified) -> None:
    result, model = pi73_verified
    before = tuple(id(step) for step in model.steps)
    content = render_model_backed_narrative_markdown(result, model)
    _, body = content.split("\n証明\n", 1)
    assert r"[R5]より, $E(\eta_{5})=\eta_{6}$." in body
    assert "[R6]より, " in body, body
    assert "[R7]より, " in body
    assert "[R5], [R6], [R7]より, " in body, body
    assert "□" in body
    assert before == tuple(id(step) for step in model.steps)


def test_unscreened_or_incomplete_model_remains_unchanged(pi73_verified) -> None:
    _, model = pi73_verified
    lines = ["使用する結果", "", "証明", "", "元の数学的表示", "", "□"]
    assert project_verified_source_and_hopf_summary(
        lines, replace(model, status=ProofSearchStatus.PARTIAL),
    ) == lines
    assert project_verified_source_and_hopf_summary(
        lines, replace(model, citations=()),
    ) == lines
    assert project_verified_source_and_hopf_summary(
        lines, replace(model, root_index=None),
    ) == lines


def test_citation_identity_not_locator_text_controls_reference(pi73_verified) -> None:
    _, model = pi73_verified
    refs = tuple(replace(c, assertion_ids=()) if c.reference.locator == "Lemma 5.7"
                 else c for c in model.citations)
    lines = ["使用する結果", "", "**[R2] Lemma 5.7.**", "", "証明", "", "□"]
    changed = project_verified_source_and_hopf_summary(
        lines, replace(model, citations=refs),
    )
    assert r"$E(\eta_2\nu')=0$." not in changed


def test_proposition_22_citation_fallback_uses_actual_given(pi73_verified) -> None:
    """Legacy model links can omit IDs, never the source ProofStep itself."""
    from phase171_r2h_prop22_cited_hopf.source import (
        ASSERTION_ID, REFERENCE_ID, TodaProp22RightFormula,
    )
    from phase175_r3r11_cited_hopf_narrative.projection import (
        _completed_scope, _source_citation,
    )
    _, model = pi73_verified
    scope = _completed_scope(model)
    assert scope is not None
    citation_only = replace(model, citations=tuple(
        replace(cite, assertion_ids=(), reference_ids=())
        if cite.reference.locator == "Proposition 2.2" else cite
        for cite in model.citations
    ))
    source = _source_citation(
        citation_only, scope, statement_type=TodaProp22RightFormula,
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        locator="Proposition 2.2", allow_provenance_fallback=True,
    )
    assert source is not None
    source_citation, source_index = source
    assert source_citation.reference.locator == "Proposition 2.2"
    original = model.steps[source_index]
    assert original.inference_rule is not None
    spoofed = replace(original, inference_rule=replace(
        original.inference_rule, name="not the verified Proposition 2.2 source",
    ))
    damaged_steps = list(citation_only.steps)
    damaged_steps[source_index] = spoofed
    damaged = replace(citation_only, steps=tuple(damaged_steps))
    assert _source_citation(
        damaged, scope, statement_type=TodaProp22RightFormula,
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        locator="Proposition 2.2", allow_provenance_fallback=True,
    ) is None
