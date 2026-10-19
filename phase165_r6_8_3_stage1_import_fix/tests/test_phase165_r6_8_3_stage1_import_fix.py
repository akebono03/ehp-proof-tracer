from pathlib import Path

from proof import ProofRule


def test_phase54_no_phase50_module_import():
    source = (Path.cwd() / "probes" / "probe_phase54_capabilities.py").read_text(encoding="utf-8")
    assert "from probes.probe_phase50_capabilities import" not in source
    assert '"phase50_final_steps"' not in source


def test_phase53_phase54_proof_contract():
    from probes.probe_phase53_capabilities import build_phase53_representative_result
    from probes.probe_phase54_capabilities import build_phase54_representative_result
    phase53 = build_phase53_representative_result()
    source = phase53["source_group_steps"][0]
    transport = phase53["transported_steps"][0]
    assert source.rule is ProofRule.INFERENCE
    assert transport.rule is ProofRule.INFERENCE
    assert source.conclusion in tuple(step.conclusion for step in transport.premises)
    assert transport.conclusion == phase53["target_relation"]
    phase54 = build_phase54_representative_result()
    assert phase54["final_steps"]
    final = phase54["final_steps"][0]
    assert final.rule is ProofRule.INFERENCE
    assert final.conclusion == phase54["final_relation"]
    assert len(final.premises) >= 2
