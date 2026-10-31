"""Pure diagnosis tests; no production imports or search mocks."""
from __future__ import annotations

from phase172_r1_renderer_audit.audit import (
    display_categories,
    duplicate_inventory,
    math_fragments,
)


def test_two_different_provenance_lines_are_not_exact_duplicates():
    lines = [
        {"proof_body_line_number": 1, "printed_text": r"[R1]より, $E(\eta_{5})=\eta_{6}$."},
        {"proof_body_line_number": 2, "printed_text": r"[R2]より, $E(\eta_{5})=\eta_{6}$."},
    ]
    observed = duplicate_inventory(lines)
    assert observed["byte_identical_nonempty_lines"] == []
    assert observed["shared_tex_fragments"] == [
        {"latex": r"E(\eta_{5})=\eta_{6}", "line_numbers": [1, 2]},
    ]


def test_exact_repetition_is_reported_without_inference():
    lines = [
        {"proof_body_line_number": 1, "printed_text": "全射である."},
        {"proof_body_line_number": 3, "printed_text": "全射である."},
    ]
    observed = duplicate_inventory(lines)
    assert observed["byte_identical_nonempty_lines"] == [
        {"text": "全射である.", "line_numbers": [1, 3]},
    ]


def test_math_extractor_requires_closed_inline_formula():
    assert math_fragments(r"$E(\eta_{5})=\eta_{6}$. $x$") == (
        r"E(\eta_{5})=\eta_{6}",
    )


def test_categories_are_non_authoritative_observations():
    assert "SURJECTIVITY" in display_categories("H の全射性を証明した.")
    assert "INTERNAL_REFERENCE_TEXT" in display_categories("DB prior")
    assert "ETA_SUSPENSION" in display_categories(r"$E(\eta_{5})=\eta_{6}$.")
