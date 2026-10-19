"""R6-8 Phase 58 cutover: reject old probe dependency and check inferred result."""
from pathlib import Path
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule


def test_phase58_does_not_import_retired_phase50_probe():
    source = (Path(__file__).resolve().parent.parent / "probes" / "probe_phase58_capabilities.py").read_text(encoding="utf-8")
    assert "from probes.probe_phase50_capabilities import" not in source
    assert "build_phase50_representative_result" not in source


def test_phase58_uses_inferred_pi43_step_from_current_search():
    from probes.probe_phase58_capabilities import build_phase58_representative_result
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    expected=search_group_from_registered_goal(n=3,k=1)
    assert expected.status is ProofSearchStatus.COMPLETE
    result=build_phase58_representative_result()
    step=result["pi4_3_step"]
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == expected.conclusion
    assert result["final_hopf_step"].rule is ProofRule.INFERENCE
