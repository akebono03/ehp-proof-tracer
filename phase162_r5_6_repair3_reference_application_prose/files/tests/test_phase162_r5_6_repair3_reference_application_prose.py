"""Phase 162 R5-6 Repair 3: concrete literature applications."""

from phase162_validated_proof_presentation import (
    _render_validated_reference_section,
    _validated_proof_body_step_lines,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def test_phase162_r5_6_repair3_hopf_surjectivity_cites_concrete_premises():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, ids = _render_validated_reference_section(presentation)
    lines = [text for _, text in _validated_proof_body_step_lines(presentation, ids)]
    matches = [line for line in lines if "は全射" in line and "\\pi_{6}^{3}" in line]
    assert len(matches) == 1
    assert "Proposition 5.1" in matches[0]
    assert "(5.3)" in matches[0]
    assert r"\pi_{6}^{5}=\mathbb{Z}/2" in matches[0]
    assert r"H(\nu')=\eta_{5}" in matches[0]


def test_phase162_r5_6_repair3_delta_injectivity_cites_components():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, ids = _render_validated_reference_section(presentation)
    lines = [text for _, text in _validated_proof_body_step_lines(presentation, ids)]
    matches = [line for line in lines if "は単射" in line and "\\pi_{5}^{5}" in line]
    assert len(matches) == 1
    assert r"\Delta(\iota_{5})=\pm2\eta_{2}" in matches[0]
    assert r"\pi_{3}^{2}=\mathbb{Z}" in matches[0]


def test_phase162_r5_6_repair3_dag_unchanged_by_rendering():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    before = tuple((id(step), tuple(id(p) for p in step.premises)) for step in presentation.nodes)
    text = render_validated_backward_proof_markdown(presentation)
    assert "### 単射性" in text and "### 全射性" in text
    assert tuple((id(step), tuple(id(p) for p in step.premises)) for step in presentation.nodes) == before
