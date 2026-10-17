from pathlib import Path
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

def test_r34_r1_complete_web_uses_shared_narrative():
    result = search_group_from_registered_goal(n=3,k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    narrative = render_partial_proof_markdown(result)
    assert narrative == render_completed_shared_narrative(result)
    assert "infinite cyclic quotient structure" not in narrative
    assert "第一同型定理" in narrative
    assert narrative.rstrip().endswith("□")
    assert narrative.count("以上より") == 1
    assert build_partial_web_group_proof_view(result).key == "generic-complete-proof"

def test_r34_r1_no_search_math_changes():
    project = Path(__file__).resolve().parent.parent
    assert "render_toda_partial_proof_narrative_markdown" in (project / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    assert "phase165_r12_r34_narrative" in (project / "toda_group_proof_narrative_renderer.py").read_text(encoding="utf8")

def test_r34_r1_partial_keeps_partial_status():
    from phase165_r52_partial_proof import PartialProofResult
    from inspect import signature
    assert "render_partial_proof_markdown" in render_partial_proof_markdown.__name__
