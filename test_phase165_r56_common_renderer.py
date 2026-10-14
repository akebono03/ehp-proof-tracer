"""R56: completed proofs use the existing common presentation pipeline."""
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def test_r56_pi32_completed_common_presentation():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    markdown = render_partial_proof_markdown(result)
    assert "証明対象" in markdown
    assert "使用する結果" in markdown
    assert "証明" in markdown
    assert "GeneratorSuspension`" not in markdown
    assert "群構造の証明状態: unknown" not in markdown


def test_r56_incomplete_preserves_partial_renderer():
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        diagnostics=("未解決",),
    )
    assert "未解決" in render_partial_proof_markdown(result)


def test_r56_adapter_rejects_incomplete():
    import pytest
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.NOT_SEARCHED)
    with pytest.raises(ValueError):
        render_completed_shared_narrative(result)
