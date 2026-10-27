"""Read-only post-patch audit of typed family and canonical 1/2-stem proofs."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative


HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = read_registered_stable_families()
    assert len(rows) == 39
    bridge = build_shared_typed_bridge()
    cases = []
    for n, k in ((8, 1), (5, 2), (6, 2), (7, 2), (8, 2)):
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        if result.status is not ProofSearchStatus.COMPLETE:
            raise AssertionError(f"pi_{n+k}^{n} lost its complete proof")
        from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
        from web_group_proof import build_standard_web_group_proof_view
        if len(contexts) != 1 or result.open_goals:
            raise AssertionError("completed proof missing screened context")
        citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        if citing_id is None:
            raise AssertionError("completed group has no citation binding")
        verify_proof_tree_for_narrative(
            result, contexts[0], citing_assertion_id=citing_id,
        )
        view = build_standard_web_group_proof_view(n, k, mode="narrative")
        if view.key != "generic-complete-proof" or view.partial_result:
            raise AssertionError("Web canonical proof regressed")
        cases.append({"n": n, "k": k, "status": result.status.value,
                      "steps": len(result.proven_steps),
                      "proof_tree_verified": True, "web_key": view.key})
        print(f"R10B_pi_{n+k}^{n}_STATUS=complete")
    output = HERE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(json.dumps({
        "phase": "169-R10B", "family_rows": len(rows), "cases": cases,
        "claim": "typed candidate registry; no source proof from DB",
        "full_pytest": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("R10B_STABLE_FAMILY_RECORDS=" + str(len(rows)))
    print("R10B_AUDIT=" + str(output / "audit.json"))
    print("R10B_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
