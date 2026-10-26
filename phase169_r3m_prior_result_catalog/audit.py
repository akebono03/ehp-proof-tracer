"""Inspect real 2-stem prior-result eligibility; do not run proof searches."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result


def build_report() -> dict:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )

    bridge = build_shared_typed_bridge()
    checks = []
    for source_n, source_k, target_n, target_k in (
        (2, 2, 3, 2),
        (3, 2, 4, 2),
        (4, 2, 5, 2),
    ):
        target_candidates = registered_group_goal_candidates(
            bridge, n=target_n, k=target_k,
        )
        target_id = (
            resolve_specialized_goal_citing_id(bridge, target_candidates[0])
            if len(target_candidates) == 1 else None
        )
        entry = {
            "source_group": f"pi_{source_n + source_k}^{source_n}",
            "target_group": f"pi_{target_n + target_k}^{target_n}",
            "target_found": len(target_candidates) == 1,
            "target_citing_id": target_id,
        }
        if target_id is not None:
            prior = resolve_prior_group_result(
                bridge,
                source_n=source_n, source_k=source_k,
                citing_assertion_id=target_id,
            )
            entry.update({
                "db_result_found": prior.relation is not None,
                "prior_result_eligible": prior.eligible,
                "source_assertion_id": prior.source_assertion_id,
                "reason": prior.reason,
                "relation_repr": repr(prior.relation),
            })
        else:
            entry.update({
                "db_result_found": None,
                "prior_result_eligible": False,
                "source_assertion_id": None,
                "reason": "target_source_not_uniquely_positioned",
                "relation_repr": None,
            })
        checks.append(entry)
    return {
        "phase": "169-R3M",
        "mode": "READ_ONLY_RESULT_CATALOG",
        "proof_search_invoked": False,
        "proof_completion_state_read": False,
        "cases": checks,
    }


def main() -> None:
    report = build_report()
    path = Path(__file__).resolve().parent / "output" / "prior_result_report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for case in report["cases"]:
        print("R3M_CASE=" + case["source_group"] + "->" + case["target_group"])
        print("R3M_RESULT_FOUND=" + str(case["db_result_found"]))
        print("R3M_SOURCE_PRIOR=" + str(case["prior_result_eligible"]))
        print("R3M_REASON=" + case["reason"])
    print("R3M_PROOF_SEARCH_INVOKED=False")
    print("R3M_PROOF_COMPLETION_REQUIRED=False")
    print("R3M_REPORT=" + str(path))
    print("R3M_AUDIT_COMPLETE=True")


if __name__ == "__main__":
    main()
