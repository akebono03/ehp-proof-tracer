"""R3-41C: migrate the two public incomplete routes, preserve explicit legacy."""
from __future__ import annotations

from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import ProofRule, ProofStep
from web_group_proof import build_web_partial_group_proof_view


def _text(view):
    """Read both inline content and Web heading rows in the rendered view."""
    return "\n".join(
        "".join(part.value for part in line.segments)
        if line.segments else line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )


def test_public_partial_web_entry_uses_common_model_without_legacy_renderer():
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(ProofStep("observed", (), ProofRule.GIVEN),),
        open_goals=("unknown",), references=("UNVERIFIED REFERENCE",),
    )
    with patch("phase165_r52_r3_web_adapter.render_partial_proof_markdown",
               side_effect=AssertionError("legacy renderer called")):
        view = build_web_partial_group_proof_view(result)
    expected = build_partial_web_group_proof_view(
        result, narrative_model=build_proof_narrative_model(result))
    assert view.rendered_lines == expected.rendered_lines
    text = _text(view)
    assert view.partial_result
    assert "部分証明・未完成" in text
    assert "observed" in text
    assert "未解決 Goal" in text and "unknown" in text
    assert any(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines)
    assert "UNVERIFIED REFERENCE" not in text
    assert "□" not in text


def test_public_unsearched_and_failed_cases_have_status_goals_diagnostics():
    for result, label in (
        (make_partial_proof_result(
            n=100, k=20, status=ProofSearchStatus.NOT_SEARCHED,
            open_goals=("target",)), "未探索"),
        (make_partial_proof_result(
            n=17, k=4, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=("no-rule",), diagnostics=("No applicable typed rule",)),
         "証明未完成"),
    ):
        view = build_web_partial_group_proof_view(result)
        content = _text(view)
        assert view.partial_result
        assert "探索状態：" + label in content
        assert "未解決 Goal" in content
        assert any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)
        assert all(str(goal) in content for goal in result.open_goals)
        if result.diagnostics:
            assert "探索診断" in content
            assert any(line.kind == "heading" and line.prefix == "探索診断"
                       for line in view.rendered_lines)
            assert "No applicable typed rule" in content
        assert "□" not in content


def test_flask_custom_missing_inputs_uses_common_model_without_legacy():
    with patch("phase165_r52_r3_web_adapter.render_partial_proof_markdown",
               side_effect=AssertionError("legacy renderer called")):
        view = build_group_proof_progress_view(n=3, k=2, goal="pending")
    text = _text(view)
    assert view.partial_result
    assert "探索状態：未探索" in text
    assert "未解決 Goal" in text and "pending" in text
    assert "探索診断" in text
    assert any(line.kind == "heading" and line.prefix == "探索診断"
               for line in view.rendered_lines)
    assert "□" not in text


def test_direct_adapter_without_model_keeps_explicit_compatibility_fallback():
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        open_goals=("unknown",),
    )
    view = build_partial_web_group_proof_view(result)
    content = _text(view)
    assert "探索状態：部分証明・未完成" in content
    assert "未解決 Goal" in content
    assert "参照情報を持つ ProofStep はありません。" in content
    assert "□" not in content


def test_public_trace_still_does_not_render_narrative():
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        open_goals=("unknown",),
    )
    assert build_web_partial_group_proof_view(result, mode="trace").rendered_lines == ()


def test_web_heading_without_segments_is_included_in_capture():
    """Heading text belongs to prefix, unlike segmented ordinary lines."""
    from types import SimpleNamespace
    from web_group_proof_common import WebGroupProofRenderedLineView

    heading = WebGroupProofRenderedLineView(
        kind="heading", indent_level=0, prefix="探索診断",
        statement_latex=None, suffix="",
    )
    ordinary = WebGroupProofRenderedLineView(
        kind="text", indent_level=0, prefix="- No applicable typed rule",
        statement_latex=None, suffix="",
    )
    view = SimpleNamespace(rendered_lines=(heading, ordinary))
    assert _text(view) == "探索診断\n- No applicable typed rule"
