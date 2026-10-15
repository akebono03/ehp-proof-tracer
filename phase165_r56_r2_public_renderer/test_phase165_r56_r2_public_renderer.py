"""Verify R56's completed typed search uses the already-existing public renderer."""
import pytest

import phase165_r56_presentation_adapter as adapter
from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_r55_nk_only_goal import search_group_from_registered_goal


def test_r56_r2_complete_calls_existing_public_renderer(monkeypatch):
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    observed = []

    def public_renderer(presentation):
        observed.append(presentation)
        assert presentation.root_step.conclusion == result.conclusion
        return "## 証明対象\n\n## 使用する結果\n\n## 証明\n\nPUBLIC_RENDERER_MARKER"

    monkeypatch.setattr(adapter, "render_toda_group_proof_narrative_markdown", public_renderer)
    assert render_partial_proof_markdown(result).endswith("PUBLIC_RENDERER_MARKER")
    assert len(observed) == 1


def test_r56_r2_actual_public_narrative_integration():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    markdown = render_partial_proof_markdown(result)
    assert "証明対象" in markdown
    assert "使用する結果" in markdown
    assert "証明" in markdown
    assert "`GeneratorSuspension`" not in markdown
    assert "出典情報は検証済み ProofStep との対応確認待ち" not in markdown
    assert "[B09]" not in markdown


def test_r56_r2_public_renderer_errors_are_not_hidden(monkeypatch):
    result = search_group_from_registered_goal(n=2, k=1)

    def raises(_presentation):
        raise ValueError("public renderer unsupported input")

    monkeypatch.setattr(adapter, "render_toda_group_proof_narrative_markdown", raises)
    with pytest.raises(ValueError, match="public renderer unsupported input"):
        render_partial_proof_markdown(result)


def test_r56_r2_incomplete_stays_fail_closed(monkeypatch):
    result = make_partial_proof_result(
        n=2, k=1,
        status=ProofSearchStatus.SEARCH_FAILED,
        diagnostics=("未解決",),
    )

    def forbidden(_presentation):
        raise AssertionError("incomplete proof reached completed renderer")

    monkeypatch.setattr(adapter, "render_toda_group_proof_narrative_markdown", forbidden)
    assert "未解決" in render_partial_proof_markdown(result)
