"""Real public projection of certified partial and complete Proof Trees."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("k", (8, 31))
def test_unsupported_given_stays_in_model_but_not_proof_body(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    model = build_proof_narrative_model(result)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert result.abstract_structure is not None
    assert len(model.steps) >= 6
    assert len(model.citations) >= 4
    assert model.steps[-1] is result.abstract_structure.proof_step
    assert model.open_goals == result.open_goals
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "TodaProp44UniversalStatement（数式表示未対応）" not in markdown
    assert "TodaLemma54TypedSource（数式表示未対応）" not in markdown
    assert "数式表示未対応" not in markdown
    assert "Proposition 4.4" in markdown
    assert "Lemma 5.4" in markdown
    assert "## 未解決 Goal" in markdown
    assert markdown.index("## 未解決 Goal") > markdown.index("- 推論:")
    assert r"\cong" in markdown
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    assert view.key == "generic-partial-proof"
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("未解決 Goal") == 1
    assert "証明済みの抽象群構造" not in headings
    shown = "\n".join(segment.value for line in view.rendered_lines
                      for segment in line.segments)
    assert "数式表示未対応" not in shown
    assert "Proposition 4.4" in shown
    assert "Lemma 5.4" in shown
    assert "、" not in shown and "。" not in shown


def test_empty_failed_search_preserves_its_actual_open_goals() -> None:
    result = search_group_from_registered_goal(n=5, k=3)
    model = build_proof_narrative_model(result)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert not model.steps
    assert model.open_goals == result.open_goals
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "参照情報を持つ ProofStep はありません" in markdown
    assert "## 未解決 Goal" in markdown
    assert "数式表示未対応" not in markdown


def test_completed_group_keeps_root_reference_and_completion() -> None:
    result = search_group_from_registered_goal(n=4, k=4)
    model = build_proof_narrative_model(result)
    assert result.status is ProofSearchStatus.COMPLETE
    assert model.root_index is not None
    assert model.steps == result.proven_steps
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "[R" in markdown and "□" in markdown
    assert "## 未解決 Goal" not in markdown
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result and not view.abstract_structure_certified
