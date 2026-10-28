"""Require a genuine complete Proof Tree and public trust-gated narrative."""
from __future__ import annotations

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    result = search_group_from_registered_goal(n=2, k=3)
    print("PHASE170_R3R5_pi_5^2_SEARCH_STATUS=", result.status, sep="", flush=True)
    print("PHASE170_R3R5_pi_5^2_PROVEN_STEPS=", len(result.proven_steps), sep="", flush=True)
    print("PHASE170_R3R5_pi_5^2_OPEN_GOALS=", len(result.open_goals), sep="", flush=True)
    print("PHASE170_R3R5_pi_5^2_DIAGNOSTICS=", repr(result.diagnostics), sep="", flush=True)
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or not result.proven_steps):
        print("PHASE170_R3R5_pi_5^2=NOT_COMPLETE", flush=True)
        return 3
    try:
        view = build_standard_web_group_proof_view(
            n=2, k=3, max_depth=2, mode="narrative", citation_source="model",
        )
    except Exception as exc:
        print(f"PHASE170_R3R5_WEB_TRUST_REJECTED={type(exc).__name__}: {exc}", flush=True)
        return 4
    print("PHASE170_R3R5_WEB_KEY=", view.key, sep="", flush=True)
    print("PHASE170_R3R5_WEB_PARTIAL=", view.partial_result, sep="", flush=True)
    print("PHASE170_R3R5_WEB_LINES=", len(view.rendered_lines), sep="", flush=True)
    if (view.key != "generic-complete-proof" or view.partial_result
            or not view.steps or not view.rendered_lines):
        return 5
    print("PHASE170_R3R5_pi_5^2=COMPLETE_AND_WEB_VERIFIED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
