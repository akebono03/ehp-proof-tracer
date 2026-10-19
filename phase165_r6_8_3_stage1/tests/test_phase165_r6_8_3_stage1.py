from proof import ProofRule
from probes.probe_phase53_capabilities import build_phase53_representative_result
from probes.probe_phase54_capabilities import build_phase54_representative_result


def test_phase53_transport_depends_on_current_derived_source():
    data = build_phase53_representative_result()
    source = data['source_group_steps'][0]
    assert source.rule is ProofRule.INFERENCE
    assert data['pi43_proof'].conclusion == source.conclusion
    assert data['toda45_steps']
    assert data['transported_steps']
    step = data['transported_steps'][0]
    assert step.rule is ProofRule.INFERENCE
    assert source.conclusion in tuple(item.conclusion for item in step.premises)
    assert step.conclusion == data['target_relation']


def test_phase54_derived_eta_group_after_transport():
    data = build_phase54_representative_result()
    assert data['final_steps']
    step = data['final_steps'][0]
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == data['final_relation']
    assert len(step.premises) >= 2
