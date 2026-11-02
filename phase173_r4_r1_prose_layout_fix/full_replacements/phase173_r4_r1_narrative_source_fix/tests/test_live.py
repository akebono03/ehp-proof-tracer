"""Active mathematical and Web render checks; executed after installation."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def test_pi74_proof_remains_complete_after_narrative_fix() -> None:
    result = search_group_from_registered_goal(n=4, k=3)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(result.proven_steps) == 7


def test_pi74_reference_and_toda56_are_rendered_as_math() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=3, max_depth=2, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    segments = tuple(s for line in view.rendered_lines for s in line.segments)
    rendered_math = tuple(s.value for s in segments if s.kind in ("inline_math", "display_math"))
    assert any(x == r"\pi_{6}^{3}" for x in rendered_math)
    assert any(r"2E\nu_4=E^2\nu'" in x for x in rendered_math)
    assert any(r"H(\nu_4)=\iota_7" in x for x in rendered_math)
    assert any(r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in x and r"\cong" in x for x in rendered_math)
    assert any(r"\Phi:\pi_6^3\oplus\pi_7^7" in x and r"\cong" in x for x in rendered_math)
    assert not any(r"\Phi(\nu',0)=" in x for x in rendered_math)
    assert not any(r"\Phi(0,\iota_7)=" in x for x in rendered_math)
    rendered_text = "\n".join(
        "".join(segment.value for segment in line.segments if segment.kind in ("text", "strong"))
        for line in view.rendered_lines
    )
    assert "Toda (5.6)" not in rendered_text
    assert "Hopf 関係により" not in rendered_text
    assert "この同型は" not in rendered_text
