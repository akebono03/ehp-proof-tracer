"""Phase 162 R5-6 Repair 2: direct source citation, no transitive inflation."""

from phase162_validated_proof_presentation import (
    _composed_validated_proof_sections,
    _direct_reference_markers,
    _render_validated_reference_section,
    _validated_main_proof_steps,
    _validated_proof_body_step_lines,
    _validated_reference_number_by_step_id,
    build_validated_backward_proof_presentation,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def test_phase162_r5_6_repair2_core_steps_cite_only_direct_literature_premises():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, reference_step_ids = _render_validated_reference_section(presentation)
    references = _validated_reference_number_by_step_id(presentation)
    core_ids = _validated_main_proof_steps(presentation)
    composed = _composed_validated_proof_sections(presentation, reference_step_ids)
    text_lines = tuple(line for _, lines in composed for line in lines)
    records = _validated_proof_body_step_lines(presentation, reference_step_ids)

    assert len(text_lines) == len(records)
    assert "を用いて、" not in "\n".join(text_lines)
    for step, prose in records:
        if id(step) not in core_ids:
            continue
        markers = _direct_reference_markers(step, references)
        if markers:
            assert prose.startswith(", ".join(markers) + "より、")
        else:
            assert not prose.startswith("[R")
        assert prose in text_lines


def test_phase162_r5_6_repair2_source_edges_and_derived_steps_unchanged():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, reference_step_ids = _render_validated_reference_section(presentation)
    nodes = tuple(id(step) for step in presentation.nodes)
    edges = tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges)
    sections = dict(_composed_validated_proof_sections(presentation, reference_step_ids))
    assert tuple(sections) == ("準備", "単射性", "全射性", "結論")
    assert tuple(id(step) for step in presentation.nodes) == nodes
    assert tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges) == edges
    assert "は単射" in "\n".join(sections["単射性"])
    assert "は全射" in "\n".join(sections["全射性"])
