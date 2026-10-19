"""Focused R3-B contracts: production Renderer only, no prose manipulation."""

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation, perform_r3b_audit
from proof import ProofRule


@pytest.fixture(scope='module')
def r3b_result(tmp_path_factory):
    return perform_r3b_audit(tmp_path_factory.mktemp('phase162_r3b'))


def test_phase162_r3b_presentation_is_original_r2_tree():
    r2, presentation = build_r3b_presentation()
    root = r2.reconstruction.final_step
    assert presentation.root_step is root
    assert root.inference_rule.name == 'phase162_group_structure_transport'
    assert root.premises[1] is r2.source_structure_step
    assert root.premises[2] is r2.generator_image_step
    assert len(presentation.nodes) == 123
    assert len(presentation.edges) == 135
    assert sum(node.proof_step.rule is ProofRule.INFERENCE for node in presentation.nodes) == 67


def test_phase162_r3b_production_renderer_returns_raw_markdown(r3b_result):
    report, markdown, rows = r3b_result
    assert report['renderer'] == 'render_toda_group_proof_narrative_markdown'
    assert report['status'] == 'RENDERED_NOT_SEMANTICALLY_CERTIFIED'
    assert report['historical_markdown_used_as_input'] is False
    assert report['specialized_pi5_3_prose_added'] is False
    assert markdown.strip()
    assert len(rows) == 123


def test_phase162_r3b_inference_reporting_never_claims_unverified_explanations(r3b_result):
    report, _, rows = r3b_result
    assert report['reason_explanation_audit_status'] == 'NOT_AUDITED'
    assert report['reason_explanation_verified_count'] == 0
    assert all(row['reason_explanation_status'] == 'NOT_AUDITED' for row in rows)
    assert sum(row['proof_rule'] == 'inference' for row in rows) == 67
