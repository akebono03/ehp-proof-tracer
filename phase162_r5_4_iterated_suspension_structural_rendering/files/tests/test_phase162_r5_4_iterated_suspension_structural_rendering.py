"""Phase 162 R5-4 structural display of iterated suspension relations."""

from expression import IteratedSuspension
from phase162_validated_proof_presentation import (
    _render_validated_backward_step,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from proof import Relation, RelationType
from repository_element_presentation import render_repository_conclusion_latex
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def test_phase162_r5_4_iterated_suspension_relation_retains_operator():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    steps = [
        step for step in presentation.nodes
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and (
            isinstance(step.conclusion.lhs, IteratedSuspension)
            or isinstance(step.conclusion.rhs, IteratedSuspension)
        )
    ]
    assert steps
    for step in steps:
        expected = "$" + render_repository_conclusion_latex(step.conclusion) + "$"
        assert _render_validated_backward_step(step) == expected
        assert "E^{" in expected


def test_phase162_r5_4_web_narrative_preserves_e2_eta3_relation():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    before_nodes = tuple(id(step) for step in presentation.nodes)
    before_edges = tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges)
    output = render_validated_backward_proof_markdown(presentation)
    _, body = output.split("## 証明", 1)
    assert r"E^{2}\eta_{3}" in body
    assert r"\eta_{5}" in body
    assert tuple(id(step) for step in presentation.nodes) == before_nodes
    assert tuple((id(edge.parent_step), id(edge.premise_step)) for edge in presentation.edges) == before_edges
