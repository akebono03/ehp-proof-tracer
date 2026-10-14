"""Targeted tests for the only public narrative entry point."""
import pytest

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def test_r57_r2_partial_uses_public_renderer(monkeypatch):
    import toda_group_proof_narrative_renderer as public
    observed = []
    actual = public.render_toda_group_proof_narrative_markdown

    def delegate(argument):
        observed.append(argument)
        return actual(argument)

    monkeypatch.setattr(public, "render_toda_group_proof_narrative_markdown", delegate)
    result = make_partial_proof_result(
        n=3,
        k=1,
        status=ProofSearchStatus.PARTIAL,
        open_goals=("unresolved premise",),
    )
    rendered = render_partial_proof_markdown(result)
    assert observed == [result]
    assert "未解決 Goal" in rendered
    assert "unresolved premise" in rendered
    assert "□" not in rendered


def test_r57_r2_incomplete_public_entry_is_fail_closed():
    result = make_partial_proof_result(
        n=4,
        k=7,
        status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unknown typed theorem",),
        diagnostics=("no matching typed inference",),
    )
    rendered = render_toda_group_proof_narrative_markdown(result)
    assert "証明未完成" in rendered
    assert "未解決 Goal" in rendered
    assert "no matching typed inference" in rendered
    assert "□" not in rendered


def test_r57_r2_complete_search_uses_existing_presentation(monkeypatch):
    import phase165_r56_presentation_adapter as adapter
    import toda_group_proof_narrative_renderer as public
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    seen = []
    real = adapter.render_completed_shared_narrative

    def observed(argument):
        seen.append(argument)
        return real(argument)

    monkeypatch.setattr(adapter, "render_completed_shared_narrative", observed)
    rendered = public.render_toda_group_proof_narrative_markdown(result)
    assert seen == [result]
    assert "使用する結果" in rendered
    assert "証明" in rendered
    assert "GeneratorSuspension" not in rendered


def test_r57_r2_public_entry_rejects_invalid_partial_type():
    from phase165_r57_r2_partial_narrative import render_incomplete_public_narrative
    with pytest.raises(TypeError):
        render_incomplete_public_narrative(None)
