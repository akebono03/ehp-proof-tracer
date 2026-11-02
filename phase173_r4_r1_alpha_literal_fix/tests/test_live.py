"""Focused browser-facing regression: pi_7^4 alpha is a valid TeX token."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def test_pi74_specialization_alpha_tex_is_not_a_control_character() -> None:
    result = search_group_from_registered_goal(n=4, k=3)
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    view = build_standard_web_group_proof_view(
        n=4, k=3, mode="narrative", max_depth=2,
        citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    segments = tuple(
        segment for line in view.rendered_lines
        for segment in line.segments
    )
    math_values = tuple(segment.value for segment in segments if segment.kind == "inline_math")
    assert r"\alpha=\nu_4" in math_values
    assert all("\x07" not in segment.value for segment in segments)
    assert all(
        not any(ord(char) < 32 and char not in "\t\n\r" for char in segment.value)
        for segment in segments
    )
    assert any(r"\Phi:\pi_6^3\oplus\pi_7^7" in segment.value for segment in segments)
