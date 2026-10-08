"""Phase 162 R5-5: composition follows validated step ancestry."""

from phase162_validated_proof_presentation import (
    _composed_validated_proof_sections,
    _render_validated_reference_section,
    _validated_proof_body_lines,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def test_phase162_r5_5_sections_preserve_all_visible_steps_in_order_per_branch():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, reference_ids = _render_validated_reference_section(presentation)
    sections = _composed_validated_proof_sections(presentation, reference_ids)
    assert tuple(label for label, _ in sections) == (
        "準備", "単射性", "全射性", "結論"
    )
    flat_lines = _validated_proof_body_lines(presentation, reference_ids)
    composed_lines = tuple(line for _, lines in sections for line in lines)
    assert len(composed_lines) == len(flat_lines)
    assert set(composed_lines) == set(flat_lines)
    assert composed_lines[-1] == flat_lines[-1]


def test_phase162_r5_5_narrative_headings_follow_proof_dependencies():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    before_nodes = tuple(id(step) for step in presentation.nodes)
    before_edges = tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges)
    text = render_validated_backward_proof_markdown(presentation)
    assert text.index("## 使用する結果") < text.index("## 証明")
    assert text.index("### 準備") < text.index("### 単射性")
    assert text.index("### 単射性") < text.index("### 全射性")
    assert text.index("### 全射性") < text.index("### 結論")
    assert r"E^{2}\eta_{3}" in text
    assert text.rstrip().endswith("□")
    assert tuple(id(step) for step in presentation.nodes) == before_nodes
    assert tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges) == before_edges
