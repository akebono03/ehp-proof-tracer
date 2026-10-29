"""Check actual Web proof closure for every requested low-range n=2 structure."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


TARGETS = (3, 4, 5, 6, 7, 8, 9, 10, 14)


def check(k: int) -> bool:
    label = f"pi_{k + 2}^2"
    result = search_group_from_registered_goal(n=2, k=k)
    print(f"PHASE170_R3R7_{label}_STATUS={result.status}", flush=True)
    print(f"PHASE170_R3R7_{label}_PROVEN_STEPS={len(result.proven_steps)}", flush=True)
    print(f"PHASE170_R3R7_{label}_OPEN_GOALS={len(result.open_goals)}", flush=True)
    if result.status is not ProofSearchStatus.COMPLETE or not result.proven_steps or result.open_goals:
        print(f"PHASE170_R3R7_{label}_DIAGNOSTICS={result.diagnostics!r}", flush=True)
        return False
    view = build_standard_web_group_proof_view(
        n=2, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    okay = (
        view.key == "generic-complete-proof"
        and not view.partial_result
        and bool(view.steps)
        and bool(view.rendered_lines)
    )
    print(f"PHASE170_R3R7_{label}_WEB_KEY={view.key}", flush=True)
    print(f"PHASE170_R3R7_{label}_WEB_PARTIAL={view.partial_result}", flush=True)
    print(f"PHASE170_R3R7_{label}={'COMPLETE_AND_WEB_VERIFIED' if okay else 'WEB_FAILED'}", flush=True)
    return okay


def main() -> int:
    failures = tuple(k for k in TARGETS if not check(k))
    if failures:
        print(f"PHASE170_R3R7_UNFINISHED_K={failures!r}", flush=True)
        return 2
    print("PHASE170_R3R7_ALL_TARGETS_COMPLETE_AND_WEB_VERIFIED=True", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
