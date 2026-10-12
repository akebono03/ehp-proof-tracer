from pathlib import Path


def test_production_wiring_retains_existing_api():
    module = Path(__file__).resolve().parents[1] / "phase165_r9_production_wiring.py"
    content = module.read_text(encoding="utf-8")
    assert "def discover_goal_search_inputs(*, proof_repository=None)" in content
    assert "build_phase165_r5_manifest_bridge(base_bridge=discovery.bridge)" in content
    assert "verified_assertion_ids=()" in content


def test_reference_policy_does_not_approve_typed_steps():
    from phase165_tex_citation_policy import TexCitationDecision
    assert TexCitationDecision.__dataclass_fields__["proof_step_eligible"].default is False
