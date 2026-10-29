"""Active Web verification of the previously missing pi_14^2 proof."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    for k in (5, 6, 8, 10, 11, 12, 14):
        result = search_group_from_registered_goal(n=2, k=k)
        status = getattr(result.status, "value", str(result.status))
        print(f"PHASE170_R3R9_k={k}_SEARCH_STATUS={status}", flush=True)
        print(f"PHASE170_R3R9_k={k}_OPEN_GOALS={len(result.open_goals)}", flush=True)
        print(f"PHASE170_R3R9_k={k}_PROVEN_STEPS={len(result.proven_steps)}", flush=True)
        if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
                or not result.proven_steps):
            print(f"PHASE170_R3R9_k={k}_DIAGNOSTICS={result.diagnostics!r}", flush=True)
            return 4
        view = build_standard_web_group_proof_view(
            n=2, k=k, max_depth=2, mode="narrative", citation_source="model",
        )
        print(f"PHASE170_R3R9_k={k}_WEB_KEY={view.key}", flush=True)
        if (view.key != "generic-complete-proof" or view.partial_result
                or not view.steps or not view.rendered_lines):
            return 5
        print(f"PHASE170_R3R9_k={k}=COMPLETE_AND_WEB_VERIFIED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
