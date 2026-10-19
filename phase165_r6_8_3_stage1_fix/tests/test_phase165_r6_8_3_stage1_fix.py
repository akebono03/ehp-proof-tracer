from pathlib import Path

from proof import ProofRule
from probes.probe_phase53_capabilities import build_phase53_representative_result
from probes.probe_phase54_capabilities import build_phase54_representative_result


def test_phase53_generic_transport_provenance():
    result = build_phase53_representative_result()
    source = result['source_group_steps'][0]
    assert source.rule is ProofRule.INFERENCE
    assert source.conclusion == result['pi43_proof'].conclusion
    assert result['toda45_steps']
    assert result['transported_steps']
    step = result['transported_steps'][0]
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == result['target_relation']
    assert source.conclusion in tuple(p.conclusion for p in step.premises)
    assert 'generic' in step.inference_rule.name.lower()


def test_phase54_transport_still_derives_eta_family_relation():
    result = build_phase54_representative_result()
    assert result['final_steps']
    step = result['final_steps'][0]
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == result['final_relation']
    assert len(step.premises) >= 2


def test_phase53_no_removed_rule_reference():
    source = (Path.cwd() / 'probes' / 'probe_phase53_capabilities.py').read_text(encoding='utf-8')
    assert 'toda_45_pi4_3_finite_cyclic_transport_inference_rule' not in source
    assert 'build_phase50_representative_result' not in source
