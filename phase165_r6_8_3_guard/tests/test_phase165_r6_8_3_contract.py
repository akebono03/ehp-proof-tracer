"""Phase 165 R6-8③: replacement contract, not a legacy return-value adapter."""
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import ProofRule, Relation


ROOT = Path(__file__).resolve().parents[2]


def test_phase53_no_legacy_phase50_builder_dependency():
    source = (ROOT / "probes" / "probe_phase53_capabilities.py").read_text(encoding="utf-8")
    assert "build_phase50_representative_result" not in source
    assert 'phase50["rules"]' not in source


def test_phase55_no_legacy_phase50_builder_dependency():
    source = (ROOT / "probes" / "probe_phase55_capabilities.py").read_text(encoding="utf-8")
    assert "build_phase50_representative_result" not in source
    assert 'phase50["rules"]' not in source


def test_phase54_no_legacy_phase50_final_steps_dependency():
    source = (ROOT / "probes" / "probe_phase54_capabilities.py").read_text(encoding="utf-8")
    assert '"phase50_final_steps"' not in source


def test_pi43_backward_proof_has_derived_root_and_no_open_goals():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is ProofSearchStatus.COMPLETE, result.diagnostics
    assert result.open_goals == ()
    assert isinstance(result.conclusion, Relation)
    roots = tuple(step for step in result.proven_steps if step.conclusion == result.conclusion)
    assert roots
    assert any(step.rule is ProofRule.INFERENCE for step in roots)
