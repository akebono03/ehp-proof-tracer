"""Live public narrative regression for the 4-source pi_7^4 proof."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def test_pi74_cited_proof_uses_short_sentence_lines() -> None:
    proof = search_group_from_registered_goal(n=4, k=3)
    assert proof.status is ProofSearchStatus.COMPLETE
    assert proof.open_goals == ()
    assert len(proof.proven_steps) == 7
    view = build_standard_web_group_proof_view(n=4, k=3, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    contents = tuple(
        "".join(segment.value for segment in row.segments)
        for row in view.rendered_lines
    )
    assert all(". " not in line for line in contents)
    text = "\n".join(contents)
    assert "Toda (5.6)" not in text
    assert "Hopf 関係により" not in text
    assert "この同型は" not in text
    maths = tuple(seg.value for row in view.rendered_lines for seg in row.segments
                  if seg.kind in ("inline_math", "display_math"))
    assert any(r"\Phi:\pi_6^3\oplus\pi_7^7" in x for x in maths)
    assert not any(r"\Phi(\nu',0)=" in x for x in maths)
    assert not any(r"\Phi(0,\iota_7)=" in x for x in maths)
