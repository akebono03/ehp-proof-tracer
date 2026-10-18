from pathlib import Path
from unittest.mock import patch

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)

def test_completed_entry_uses_original_adapter_without_model_route():
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    with patch("phase165_r56_presentation_adapter.render_completed_shared_narrative",return_value="RESTORED") as target:
        with patch("phase165_renderer_narrative_model.build_narrative_proof_model",side_effect=AssertionError("model detour called")):
            assert render_partial_proof_markdown(result)=="RESTORED"
    target.assert_called_once_with(result)

def test_incomplete_entry_uses_canonical_partial_renderer_without_model_route():
    result=make_partial_proof_result(n=2,k=1,status=ProofSearchStatus.NOT_SEARCHED)
    with patch("toda_group_proof_narrative_renderer.render_toda_partial_proof_narrative_markdown",return_value="PARTIAL") as target:
        with patch("phase165_renderer_narrative_model.build_narrative_proof_model",side_effect=AssertionError("model detour called")):
            assert render_partial_proof_markdown(result)=="PARTIAL"
    target.assert_called_once_with(result)

def test_no_r57_r21_model_dispatch_in_public_entry():
    path=Path(__file__).resolve().parent.parent/"phase165_r52_partial_proof.py"
    source=path.read_text(encoding="utf8")
    function=source.split("def render_partial_proof_markdown(",1)[1]
    assert "render_narrative_proof_model" not in function
    assert "build_narrative_proof_model" not in function

def test_pi32_restored_narrative_is_mathematical():
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result=search_group_from_registered_goal(n=2,k=1)
    rendered=render_partial_proof_markdown(result)
    assert "GeneratorSuspension（数式表示未対応）" not in rendered
    assert "使用する結果" in rendered
    assert "証明" in rendered
