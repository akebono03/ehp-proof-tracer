"""Lightweight tests for the R7-B read-only classification helpers."""
from audit_r7_b import _category, _paragraphs, _stats


def test_r7_b_tracks_suspect_paragraphs_without_mutating_math():
    paragraphs = _paragraphs("$\\pi_{3}^{2}$\n\n$\\pi_{n + 1}^{n}$")
    assert len(paragraphs) == 2
    assert _category(paragraphs[0]) == ("pi3_2",)
    assert _category(paragraphs[1]) == ("stable_generic",)


def test_r7_b_counts_target_and_reference_context_separately():
    markdown = "$\\pi_{5}^{3}$\n\n$\\pi_{4}^{3}$\n\n$\\pi_{4}^{3}$"
    counts = _stats(markdown)
    assert counts["target_pi5_3"] == 1
    assert counts["pi4_3"] == 2
