"""Focused Phase 162 R3-2 fixed statement / proof internal display checks."""

from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    build_validated_proof_reference_entries,
    render_validated_backward_proof_markdown,
    _render_validated_backward_step,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture
from toda_literature_statement_boundary import (
    TodaLiteratureStatementClassification,
    classify_toda_literature_statement_step,
)


def test_phase162_r3_2_reference_is_only_fixed_statements():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    entries = build_validated_proof_reference_entries(presentation)
    assert entries
    for entry in entries:
        assert entry.reference.locator
        for step in entry.proof_steps:
            boundary = classify_toda_literature_statement_step(step)
            assert boundary.classification is TodaLiteratureStatementClassification.FIXED_STATEMENT
            assert boundary.reference_locator == entry.reference.locator


def test_phase162_r3_2_fixed_statements_are_outside_proof_body():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    entries = build_validated_proof_reference_entries(presentation)
    rendered = render_validated_backward_proof_markdown(presentation)
    reference, body = rendered.split("## 証明", 1)
    assert "## 使用する結果" in reference
    assert "---" in reference
    assert body.rstrip().endswith("□")
    for entry in entries:
        assert entry.reference.locator in reference
        for step in entry.proof_steps:
            statement = _render_validated_backward_step(step)
            assert statement in reference
            assert statement not in body.splitlines()


def test_phase162_r3_2_proof_internal_stays_in_body():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    rendered = render_validated_backward_proof_markdown(presentation)
    reference, body = rendered.split("## 証明", 1)
    internal = [
        step for step in presentation.nodes
        if (boundary := classify_toda_literature_statement_step(step)) is not None
        and boundary.classification is TodaLiteratureStatementClassification.PROOF_INTERNAL
    ]
    assert internal
    for step in internal:
        assert _render_validated_backward_step(step) in body
    assert _render_validated_backward_step(presentation.root_step) in body
