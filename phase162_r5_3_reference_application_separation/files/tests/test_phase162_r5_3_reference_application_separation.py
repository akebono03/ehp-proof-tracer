"""Phase 162 R5-3: provenance-driven source-to-application citations."""

from phase162_validated_proof_presentation import (
    _direct_reference_markers,
    _render_validated_reference_section,
    _validated_proof_body_lines,
    _validated_reference_number_by_step_id,
    build_validated_backward_proof_presentation,
    build_validated_proof_reference_entries,
    render_validated_backward_proof_markdown,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def test_phase162_r5_3_direct_references_follow_proofstep_identity():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    reference_map = _validated_reference_number_by_step_id(presentation)
    entries = build_validated_proof_reference_entries(presentation)
    assert reference_map
    for entry in entries:
        for source_step in entry.proof_steps:
            assert reference_map[id(source_step)] == entry.number
    directly_using_steps = [
        step for step in presentation.nodes
        if any(id(premise) in reference_map for premise in step.premises)
    ]
    assert directly_using_steps
    for step in directly_using_steps:
        expected = tuple(
            f"[R{number}]" for number in sorted({
                reference_map[id(premise)] for premise in step.premises
                if id(premise) in reference_map
            })
        )
        assert _direct_reference_markers(step, reference_map) == expected
    for step in presentation.nodes:
        if not any(id(p) in reference_map for p in step.premises):
            assert _direct_reference_markers(step, reference_map) == ()


def test_phase162_r5_3_reference_general_forms_and_applied_body_separate():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    original_node_ids = tuple(id(step) for step in presentation.nodes)
    original_edge_ids = tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges)
    rendered = render_validated_backward_proof_markdown(presentation)
    reference, body = rendered.split("## 証明", 1)
    assert r"E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}" in reference
    assert r"E^{n-3}" not in reference
    assert "[R" in body
    assert "より、" in body
    assert body.rstrip().endswith("□")
    assert tuple(id(step) for step in presentation.nodes) == original_node_ids
    assert tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges) == original_edge_ids


def test_phase162_r5_3_body_only_cites_numbered_direct_premises():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, fixed_ids = _render_validated_reference_section(presentation)
    lines = _validated_proof_body_lines(presentation, fixed_ids)
    reference_map = _validated_reference_number_by_step_id(presentation)
    assert any("[R" in line for line in lines)
    assert all(
        marker in {f"[R{number}]" for number in reference_map.values()}
        for line in lines for marker in __import__("re").findall(r"\[R\d+\]", line)
    )
    assert all("[R" not in line or "より、" in line for line in lines)
