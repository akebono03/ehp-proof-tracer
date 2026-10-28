"""Focused, pure tests for text metrics; actual proof is audited separately."""
from __future__ import annotations

import pytest

from phase169_r10ei_cyclic_narrative_residual_audit.diagnostics import (
    CASES, assess_case, extra_duplicate_occurrences,
    image_formula_occurrences, validate_coverage,
)


def test_r10ei_case_coverage_is_exactly_reviewed_6_and_10_stem():
    assert validate_coverage()
    assert [(case.n, case.k) for case in CASES] == [(22, 6), (22, 10)]
    assert [case.label for case in CASES] == ["pi_28^22", "pi_32^22"]


def test_r10ei_math_formula_extraction_is_citation_independent():
    text = (
        r"[R3]より, $E(\eta_{12})=\eta_{13}$." "\n"
        r"[R4]より, $E(\eta_{12})=\eta_{13}$." "\n"
        r"$E(\mu_{13})=\mu_{14}$."
    )
    rows = image_formula_occurrences(text)
    assert len(rows) == 2
    assert extra_duplicate_occurrences(rows) == 1
    assert {row["copies"] for row in rows} == {1, 2}


def test_r10ei_unbounded_generator_formula_not_a_one_step_equation():
    text = r"$E^{10}(\eta_{12}\mu_{13})=\eta_{22}\mu_{23}$"
    assert image_formula_occurrences(text) == ()


def test_r10ei_rejects_non_string_input():
    with pytest.raises(TypeError, match="markdown"):
        image_formula_occurrences(None)


def test_r10ei_assessment_distinguishes_search_from_presentation():
    first, second = CASES
    assert assess_case("complete", "PASS", True, 0, first) == "PASS"
    assert assess_case("complete", "PASS", False, 10, second) == "PASS"
    assert assess_case("partial", "NOT_APPLICABLE_INCOMPLETE", True, 0, first) == "PROOF_VERIFICATION_FAILED"
    assert assess_case("complete", "PASS", False, 0, first) == "PROJECTION_BEHAVIOR_CHANGED"
    assert assess_case("complete", "PASS", False, 9, second) == "NARRATIVE_DUPLICATES_CHANGED"
