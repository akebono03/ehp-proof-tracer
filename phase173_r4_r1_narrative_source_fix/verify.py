"""Read-only active Web verification for the corrected pi_7^4 narrative."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    result = search_group_from_registered_goal(n=4, k=3)
    view = build_standard_web_group_proof_view(
        n=4, k=3, mode="narrative", max_depth=2, citation_source="model",
    )
    segments = tuple(segment for line in view.rendered_lines for segment in line.segments)
    math = tuple(item.value for item in segments if item.kind in ("inline_math", "display_math"))
    strings = tuple(item.value for item in segments if item.kind in ("text", "strong"))
    text = "\n".join(strings)
    checks = {
        "complete": result.status is ProofSearchStatus.COMPLETE and not result.open_goals,
        "public_web_complete": view.key == "generic-complete-proof" and not view.partial_result,
        "four_references": all(f"[R{i}]" in text for i in range(1, 5)),
        "prop44_iso": any(r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in x and r"\cong" in x for x in math),
        "lemma54_hopf": any(r"H(\nu_4)=\iota_7" in x for x in math),
        "lemma54_double": any(r"2E\nu_4=E^2\nu'" in x for x in math),
        "prior_tex": any(r"\pi_{6}^{3}" in x for x in math),
        "toda56_iso": any(r"\Phi:\pi_6^3\oplus\pi_7^7" in x and r"\cong" in x for x in math),
        "generator_images": any(r"\Phi(\nu',0)=E\nu'" in x for x in math) and any(r"\Phi(0,\iota_7)=\nu_4" in x for x in math),
        "root_conclusion": any(r"\pi_7^4\cong\mathbb{Z}" in x and r"\mathbb{Z}/4" in x for x in math),
        "no_escaped_prior_latex": r"\pi\_" not in text,
    }
    for name, state in checks.items():
        print(f"PHASE173_R4_R1_NARRATIVE_{name.upper()}={state}")
    print("PHASE173_R4_R1_NARRATIVE_WEB_KEY=" + view.key)
    print("PHASE173_R4_R1_NARRATIVE_WEB_LINES=" + str(len(view.rendered_lines)))
    if not all(checks.values()):
        raise RuntimeError("The public pi_7^4 narrative does not meet source and TeX gates")
    print("PHASE173_R4_R1_NARRATIVE_VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
