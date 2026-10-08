"""Focused checks for fixed general forms and provenance-preserving application."""
from dataclasses import replace

import pytest

from toda_general_reference_schema import (
    GeneralReferenceComponent,
    GeneralReferenceStatement,
    get_general_reference_statement,
    render_general_reference_statement_lines,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture
from toda_literature_statement_boundary import get_toda_fixed_statement_components


def test_phase162_r5_2_catalog_components_match_existing_boundary():
    for locator in ("(4.5)", "(5.3)", "Proposition 5.1"):
        general = get_general_reference_statement(locator)
        assert general is not None
        assert {c.component_key for c in general.components} == {
            c.component_key for c in get_toda_fixed_statement_components(locator)
        }


def test_phase162_r5_2_general_45_is_not_specialized():
    lines = render_general_reference_statement_lines("(4.5)")
    assert lines is not None
    assert r"n\ge k+2" in lines[0]
    assert r"m\ge n" in lines[0]
    assert r"E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}" in lines[0]
    assert r"E^{n-3}" not in lines[0]


def test_phase162_r5_2_nu_prime_definition_is_in_reference():
    lines = render_general_reference_statement_lines("(5.3)")
    assert lines is not None
    assert any(r"\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}" in line for line in lines)
    assert any(r"H(\nu')=\eta_{5}" in line for line in lines)


def test_phase162_r5_2_web_source_keeps_verified_ancestry():
    validated = _validated_fixture()
    presentation = build_validated_backward_proof_presentation(validated)
    original_ids = tuple(id(step) for step in presentation.nodes)
    markdown = render_validated_backward_proof_markdown(presentation)
    reference, proof = markdown.split("## 証明", 1)
    assert "**[R2] (4.5).**" in reference
    assert r"E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}" in reference
    assert r"\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}" in reference
    assert proof.rstrip().endswith("□")
    assert tuple(id(step) for step in presentation.nodes) == original_ids
    assert all(edge.parent_step.premises[edge.premise_index] is edge.premise_step for edge in presentation.edges)


def test_phase162_r5_2_unknown_locator_uses_existing_fallback():
    assert get_general_reference_statement("Unknown") is None
    assert render_general_reference_statement_lines("Unknown") is None


def test_phase162_r5_2_schema_rejects_duplicate_components():
    component = GeneralReferenceComponent("duplicate", "x=y")
    with pytest.raises(ValueError, match="unique"):
        GeneralReferenceStatement("test", (component, component))
