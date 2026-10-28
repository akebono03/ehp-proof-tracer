"""Fail closed unless pi_7^2 genuinely completes via the public Web route."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def check(n: int, k: int, *, required: bool) -> bool:
    name = f"pi_{n+k}^{n}"
    result = search_group_from_registered_goal(n=n, k=k)
    print(f"PHASE170_R3R6_{name}_SEARCH_STATUS={result.status}", flush=True)
    print(f"PHASE170_R3R6_{name}_PROVEN_STEPS={len(result.proven_steps)}", flush=True)
    print(f"PHASE170_R3R6_{name}_OPEN_GOALS={len(result.open_goals)}", flush=True)
    if result.status is not ProofSearchStatus.COMPLETE:
        print(f"PHASE170_R3R6_{name}=UNFINISHED", flush=True)
        return not required
    if not result.proven_steps or result.open_goals:
        print(f"PHASE170_R3R6_{name}=INVALID_COMPLETION", flush=True)
        return False
    view = build_standard_web_group_proof_view(
        n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    print(f"PHASE170_R3R6_{name}_WEB_KEY={view.key}", flush=True)
    print(f"PHASE170_R3R6_{name}_WEB_PARTIAL={view.partial_result}", flush=True)
    print(f"PHASE170_R3R6_{name}_WEB_LINES={len(view.rendered_lines)}", flush=True)
    okay = (view.key == "generic-complete-proof" and not view.partial_result
            and bool(view.steps) and bool(view.rendered_lines))
    print(f"PHASE170_R3R6_{name}={'COMPLETE_AND_WEB_VERIFIED' if okay else 'WEB_VERIFICATION_FAILED'}", flush=True)
    return okay


def main() -> int:
    if not check(2, 3, required=True):
        return 2
    if not check(2, 5, required=True):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
