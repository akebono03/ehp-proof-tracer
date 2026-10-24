"""Focused preservation tests for incomplete, model-backed narratives."""
from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, ProofStep


def _render(result):
    model = build_proof_narrative_model(result)
    return model, render_model_backed_narrative_markdown(result, model)


def _web_text(view):
    return "\n".join(
        segment.value
        for line in view.rendered_lines
        for segment in line.segments
    )


def test_not_searched_retains_status_goal_and_target_without_qed():
    result = make_partial_proof_result(
        n=100, k=20, status=ProofSearchStatus.NOT_SEARCHED,
        open_goals=("target",),
    )
    model, text = _render(result)
    assert model.status is ProofSearchStatus.NOT_SEARCHED
    assert model.target == result.target
    assert model.open_goals == ("target",)
    assert model.diagnostics == ()
    assert "## 証明対象" in text
    assert r"\pi_{120}^{100}" in text
    assert "探索状態：未探索" in text
    assert "## 未解決 Goal" in text
    assert "- target" in text
    assert "参照情報を持つ ProofStep はありません。" in text
    assert "□" not in text


def test_partial_retains_every_observed_step_even_with_open_premise():
    given = ProofStep("observed", (), ProofRule.GIVEN)
    inference = ProofStep("derived", ("pending",), ProofRule.INFERENCE)
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(given, inference), open_goals=("pending",),
        references=("Unscreened label",),
    )
    model, text = _render(result)
    assert model.steps == (given, inference)
    assert model.root_index is None
    assert "部分証明・未完成" in text
    assert "- 与件: observed" in text
    assert "- 推論: derived" in text
    assert "- pending" in text
    assert "Unscreened label" not in text
    assert "□" not in text


def test_search_failed_retains_only_observed_diagnostics():
    result = make_partial_proof_result(
        n=17, k=4, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("no-rule",), diagnostics=("No applicable typed rule",),
    )
    model, text = _render(result)
    assert model.status is ProofSearchStatus.SEARCH_FAILED
    assert model.diagnostics == ("No applicable typed rule",)
    assert "探索状態：証明未完成" in text
    assert "## 未解決 Goal" in text
    assert "- no-rule" in text
    assert "## 探索診断" in text
    assert "- No applicable typed rule" in text
    assert "□" not in text


def test_partial_model_mismatch_fails_closed():
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        open_goals=("pending",),
    )
    model = build_proof_narrative_model(result)
    for altered in (
        replace(model, status=ProofSearchStatus.NOT_SEARCHED),
        replace(model, open_goals=()),
        replace(model, target=None),
    ):
        with pytest.raises(ValueError, match="partial state must match"):
            render_model_backed_narrative_markdown(result, altered)


def test_explicit_model_web_adapter_shows_partial_content():
    step = ProofStep("observed", (), ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(step,), open_goals=("unknown",),
    )
    model = build_proof_narrative_model(result)
    view = build_partial_web_group_proof_view(result, narrative_model=model)
    text = _web_text(view)
    assert view.partial_result
    assert "部分証明・未完成" in text
    assert "observed" in text
    assert "未解決 Goal" in text
    assert "unknown" in text
    assert "□" not in text


def test_legacy_model_free_adapter_remains_available():
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        open_goals=("unknown",),
    )
    view = build_partial_web_group_proof_view(result)
    assert view.partial_result
    assert "未解決 Goal" in _web_text(view)
