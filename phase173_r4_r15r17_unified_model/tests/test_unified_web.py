"""Phase 173 R15R17: one certified Model, one Reference and one Renderer."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_12_body_binding import build_narrative_body_lines
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import verified_tree_postorder
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _group_proof_statement_latex


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_verified_abstract_root_is_inside_one_canonical_model(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    structure = result.abstract_structure
    assert structure is not None
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    model = build_proof_narrative_model(result)
    evidence = verified_tree_postorder(structure.proof_step)
    assert all(any(step is item for item in model.steps) for step in evidence)
    assert model.steps[-1] is structure.proof_step
    assert model.root_index is None
    assert model.status is result.status
    assert model.open_goals == result.open_goals
    assert model.diagnostics == result.diagnostics
    assert len(model.citations) >= 4
    assert len(build_narrative_body_lines(result, model)) >= 1
    latex, fallback = _group_proof_statement_latex(structure.proof_step.conclusion)
    assert fallback is None and latex is not None
    assert r"\cong" in latex
    markdown = render_model_backed_narrative_markdown(result, model)
    assert markdown.count("## 使用する結果") == 1
    assert "Proposition 4.4" in markdown
    assert "Lemma 5.4" in markdown
    assert "DB prior: sphere.csv" in markdown
    assert r"\cong" in markdown
    assert "### 検証済み証明木の Reference" not in markdown
    assert "## 証明済みの抽象群構造" not in markdown
    assert "参照情報を持つ ProofStep はありません" not in markdown
    assert markdown.count("## 未解決 Goal") == 1


@pytest.mark.parametrize("k", (8, 31))
def test_public_web_uses_one_reference_and_preserves_named_open_goals(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    assert view.abstract_structure_certified
    assert len(view.steps) >= 4
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("未解決 Goal") == 1
    assert "検証済み証明木の Reference" not in headings
    assert "証明済みの抽象群構造" not in headings
    joined = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in joined
    assert "Lemma 5.4" in joined
    assert "、" not in joined and "。" not in joined


def test_uncertified_failed_search_does_not_gain_proof_steps() -> None:
    result = search_group_from_registered_goal(n=5, k=3)
    assert result.abstract_structure is None
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.status is ProofSearchStatus.SEARCH_FAILED
    assert model.open_goals
    view = build_standard_web_group_proof_view(n=5, k=3, mode="narrative")
    assert view.partial_result
    assert not view.abstract_structure_certified
    assert not any("Proposition 4.4" in segment.value
                   for line in view.rendered_lines for segment in line.segments)


def test_completed_group_keeps_original_model_and_citations() -> None:
    result = search_group_from_registered_goal(n=4, k=4)
    model = build_proof_narrative_model(result)
    assert result.status is ProofSearchStatus.COMPLETE
    assert model.steps == result.proven_steps
    assert model.root_index is not None
    assert model.abstract_structure is None
    view = build_standard_web_group_proof_view(n=4, k=4, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert not view.abstract_structure_certified
    assert any("[R" in segment.value
               for line in view.rendered_lines for segment in line.segments)


def test_tampered_unified_model_fails_closed() -> None:
    goal = exact_prior_database_result(4, 8)
    result = search_group_from_registered_goal(n=4, k=8, goal=goal)
    model = build_proof_narrative_model(result)
    with pytest.raises(ValueError, match="verified searched and certified trees"):
        build_narrative_body_lines(result, replace(model, steps=result.proven_steps))


def test_public_route_renders_one_narrative_only(monkeypatch) -> None:
    import phase168_r3_5_model_renderer as renderer
    import phase173_r4_r15r16r3_staged_guard_fix.tree_adapter as separate

    invocations = []
    original = renderer.render_model_backed_narrative_markdown

    def recorded(result, model):
        invocations.append(model)
        return original(result, model)

    def forbidden_secondary_render(target, root):
        raise AssertionError("a second verified-tree Narrative is forbidden")

    monkeypatch.setattr(renderer, "render_model_backed_narrative_markdown", recorded)
    monkeypatch.setattr(separate, "render_verified_tree_progress", forbidden_secondary_render)
    view = build_standard_web_group_proof_view(
        n=4, k=8, mode="narrative", citation_source="model",
    )
    assert view.partial_result
    assert len(invocations) == 1
    assert invocations[0].abstract_structure is not None
