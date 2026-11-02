"""Verify proof-cited pi_7^4 prose and sentence boundaries after installation."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    proof = search_group_from_registered_goal(n=4, k=3)
    view = build_standard_web_group_proof_view(
        n=4, k=3, mode="narrative", max_depth=2, citation_source="model",
    )
    rendered = tuple(
        "".join(segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    math = tuple(
        segment.value for line in view.rendered_lines for segment in line.segments
        if segment.kind in ("inline_math", "display_math")
    )
    prose = "\n".join(
        segment.value for line in view.rendered_lines for segment in line.segments
        if segment.kind in ("text", "strong")
    )
    checks = {
        "complete": proof.status is ProofSearchStatus.COMPLETE and not proof.open_goals
                    and len(proof.proven_steps) == 7,
        "web_complete": view.key == "generic-complete-proof" and not view.partial_result,
        "reference_count": all(f"[R{i}]" in prose for i in range(1, 5))
                           and "[R5]" not in prose,
        "prop44_isomorphism": any(r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in m
                                  and r"\cong" in m for m in math),
        "lemma54": any(r"H(\nu_4)=\iota_7" in m for m in math)
                   and any(r"2E\nu_4=E^2\nu'" in m for m in math),
        "derived_isomorphism": any(r"\Phi:\pi_6^3\oplus\pi_7^7" in m
                                  and r"\cong" in m for m in math),
        "correct_alpha": r"\alpha=\nu_4" in math,
        "no_uncited_56_label": "Toda (5.6)" not in prose,
        "no_hopf_repetition": "Hopf 関係により" not in prose,
        "no_generator_images": not any(r"\Phi(\nu',0)=" in m or
                                       r"\Phi(0,\iota_7)=" in m for m in math),
        "sentence_breaks": all(". " not in line for line in rendered),
        "no_control_chars": all(
            ord(ch) >= 32 or ch in "\n\r\t"
            for line in rendered for ch in line
        ),
        "has_final_conclusion": any(r"\pi_7^4\cong\mathbb{Z}" in m and
                                    r"\mathbb{Z}/4" in m for m in math),
    }
    for label, passed in checks.items():
        print(f"PHASE173_R4_R1_PROSE_{label.upper()}={passed}")
    if not all(checks.values()):
        raise RuntimeError("pi_7^4 cited narrative prose audit failed")
    print("PHASE173_R4_R1_PROSE_VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
