"""Focused Phase 162 R3-2 fixed statement / proof internal display checks."""

from tests.phase162_r5_6_reference_test_utils import assert_composed_steps_preserved


from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    build_validated_proof_reference_entries,
    render_validated_backward_proof_markdown,
    _render_validated_backward_step,
    _validated_proof_body_lines,
    _composed_validated_proof_sections,
    _is_display_tautology,
    _fixed_statement_reuse_visible_ids,
    _render_validated_reference_section,
)
from proof import ProofRule
from toda_general_reference_schema import render_general_reference_statement_lines
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
    fixed_ids = {
        id(step)
        for entry in entries
        for step in entry.proof_steps
    }
    for entry in entries:
        assert entry.reference.locator in reference
        registered = render_general_reference_statement_lines(entry.reference.locator)
        if registered is not None:
            # The fixed source's general formula is independent of the
            # instantiated conclusions held by its ProofStep objects.
            assert all(line in reference for line in registered)
        else:
            for step in entry.proof_steps:
                statement = _render_validated_backward_step(step)
                assert statement.rstrip(".") in reference

    # Compare the entire emitted inference sequence against the non-fixed
    # ProofStep objects. Equal strings from *other* inference steps are valid:
    # textual exclusion would confuse distinct proof identities.
    actual_body_statements = [
        line for line in body.splitlines()
        if line and line != "□"
    ]
    sections = _composed_validated_proof_sections(
        presentation, frozenset(fixed_ids)
    )
    expected_body_statements = [
        line
        for heading, prose_lines in sections
        for line in (
            (("### " + heading,) if heading != "証明" else ()) + prose_lines
        )
    ]
    assert actual_body_statements == expected_body_statements
    assert_composed_steps_preserved(
        [line for _, prose_lines in sections for line in prose_lines],
        _validated_proof_body_lines(presentation, frozenset(fixed_ids)),
    )




def test_phase162_r3_2_proof_internal_stays_in_body():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    rendered = render_validated_backward_proof_markdown(presentation)
    reference, body = rendered.split("## 証明", 1)
    _, fixed_ids = _render_validated_reference_section(presentation)
    visible_ids = _fixed_statement_reuse_visible_ids(presentation, fixed_ids)
    internal = [
        step for step in presentation.nodes
        if (boundary := classify_toda_literature_statement_step(step)) is not None
        and boundary.classification is TodaLiteratureStatementClassification.PROOF_INTERNAL
    ]
    assert internal
    suppressed = []
    for step in internal:
        if id(step) not in visible_ids:
            # The source is cited at a fixed-statement boundary. Its proof
            # remains in the DAG, but its exclusive ancestry is not displayed.
            suppressed.append(step)
            assert any(node is step for node in presentation.nodes)
            continue
        assert (
            _render_validated_backward_step(step) in body
            or any(
                other is not step and other.conclusion == step.conclusion
                for other in presentation.nodes
            )
            or (
                getattr(step.conclusion, "lhs", object())
                == getattr(step.conclusion, "rhs", None)
            )
            or _is_display_tautology(
                step, _render_validated_backward_step(step)
            )
        )
    assert suppressed, "Fixture must exercise fixed-statement source suppression"
    assert "(5.3)" in reference
    assert _render_validated_backward_step(presentation.root_step) in body


def test_phase162_r3_2_display_tautology_retains_proof_step_ancestry():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    rendered = render_validated_backward_proof_markdown(presentation)
    _, body = rendered.split("## 証明", 1)

    # An internal inference may render as a reflexive expression in older
    # renderers. R5-4 preserves the iterated suspension operator, so this
    # test must not require such suppressed lines to exist.
    internal_steps = [
        step for step in presentation.nodes
        if (boundary := classify_toda_literature_statement_step(step)) is not None
        and boundary.classification is TodaLiteratureStatementClassification.PROOF_INTERNAL
    ]
    assert internal_steps

    hidden_internal_steps = [
        step for step in internal_steps
        if _is_display_tautology(step, _render_validated_backward_step(step))
    ]
    assert all(
        _render_validated_backward_step(step) not in body.splitlines()
        for step in hidden_internal_steps
    )
    assert all(
        any(node is step for node in presentation.nodes)
        for step in internal_steps
    )

    # In particular, the former η₅ = η₅ display must retain E²η₃ = η₅.
    assert r"E^{2}\eta_{3}" in body
    assert r"\eta_{5}" in body
    assert any(
        any(premise is step for node in presentation.nodes for premise in node.premises)
        for step in internal_steps
    )
