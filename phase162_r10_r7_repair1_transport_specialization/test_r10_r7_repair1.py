from tests.test_phase143_19_method_evidence import _method_evidence_data
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from toda_group_proof_narrative_renderer import _render_group_proof_narrative_latex
from toda_group_proof_narrative_transport_link import render_suspension_transport_link


def test_r10_r7_repair1_existing_stable_specialization_keeps_link():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    root = presentation.root_step
    assert root.inference_rule is None
    assert render_suspension_transport_link(root, _render_group_proof_narrative_latex) is not None


def test_r10_r7_repair1_reconstructed_pi53_excludes_ancestor_link():
    root = build_phase162_pi5_3_web_replay(max_depth=40).root_step
    assert root.inference_rule is not None
    assert render_suspension_transport_link(root, _render_group_proof_narrative_latex) is None


def test_r10_r7_repair1_stable_base_still_has_no_link():
    presentation, _, _, _ = _method_evidence_data(3, 1)
    assert render_suspension_transport_link(presentation.root_step, _render_group_proof_narrative_latex) is None
