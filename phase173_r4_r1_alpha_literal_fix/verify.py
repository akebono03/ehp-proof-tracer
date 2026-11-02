"""Verify both the fixed TeX token and the original public proof status."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    result = search_group_from_registered_goal(n=4, k=3)
    view = build_standard_web_group_proof_view(
        n=4, k=3, mode="narrative", max_depth=2,
        citation_source="model",
    )
    segments = tuple(segment for line in view.rendered_lines for segment in line.segments)
    math_values = tuple(segment.value for segment in segments if segment.kind == "inline_math")
    checks = {
        "complete": result.status is ProofSearchStatus.COMPLETE and not result.open_goals,
        "web_complete": view.key == "generic-complete-proof" and not view.partial_result,
        "alpha_tex": r"\alpha=\nu_4" in math_values,
        "no_control_chars": all(
            not any(ord(char) < 32 and char not in "\t\n\r" for char in segment.value)
            for segment in segments
        ),
        "toda56": any(r"\Phi:\pi_6^3\oplus\pi_7^7" in item.value for item in segments),
    }
    for name, passed in checks.items():
        print(f"PHASE173_R4_R1_ALPHA_{name.upper()}={passed}")
    if not all(checks.values()):
        raise RuntimeError("The pi_7^4 alpha parameter is not valid rendered TeX")
    print("PHASE173_R4_R1_ALPHA_VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
