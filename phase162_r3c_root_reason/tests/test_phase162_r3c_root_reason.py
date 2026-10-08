"""R3-C focused checks for genuine three-premise transport reasoning."""

from dataclasses import replace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from proof import ProofRule
from toda_group_structure_transport_reason import render_group_structure_transport_reason
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


def test_phase162_r3c_transport_reason_uses_actual_three_premises(presentation):
    root = presentation.root_step
    assert root.inference_rule.name == 'phase162_group_structure_transport'
    assert len(root.premises) == 3
    reason = render_group_structure_transport_reason(root)
    assert reason is not None
    assert '同型' in reason
    assert '生成元' in reason
    assert '巡回群' in reason
    assert '位数' in reason


def test_phase162_r3c_public_renderer_contains_root_reason(presentation):
    reason = render_group_structure_transport_reason(presentation.root_step)
    result = render_toda_group_proof_narrative_markdown(presentation)
    assert result.count(reason) == 1
    assert result.index(reason) < result.rfind('以上より,')
    assert result.rstrip().endswith('□')


def test_phase162_r3c_rejects_tampered_transport_conclusion(presentation):
    root = presentation.root_step
    tampered = replace(root, conclusion=root.premises[1].conclusion)
    with pytest.raises(ValueError, match='conclusion does not follow'):
        render_group_structure_transport_reason(tampered)


def test_phase162_r3c_ignores_unrelated_inference(presentation):
    unrelated = presentation.root_step.premises[0]
    assert unrelated.rule is ProofRule.INFERENCE
    assert render_group_structure_transport_reason(unrelated) is None
