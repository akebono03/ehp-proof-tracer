"""Focused separator and group-transport audit; no fabricated completion."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase169_r10e4_ordered_db_prior.db_prior import (
    _has_explicit_row, admitted_db_step, exact_prior_database_result, group_coordinates,
    DEFAULT_CSV,
)

OUTPUT = Path(__file__).resolve().parent / "output"
CASES = ((14, 7), (14, 6), (15, 7), (8, 4), (8, 6), (15, 8), (15, 9))


def main() -> None:
    bridge = build_shared_typed_bridge()
    report = []
    for n, k in CASES:
        source_n = k + 2
        source = exact_prior_database_result(source_n, k)
        zero = database_zero_group_goal_candidates(n=n, k=k)
        goal_candidates = zero or registered_group_goal_candidates(bridge, n=n, k=k)
        admitted = None
        if source is not None and len(goal_candidates) == 1:
            admitted = admitted_db_step(source, proof_target=goal_candidates[0], bridge=bridge)
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        item = {
            "n": n, "k": k, "base_n": source_n,
            "base_row_present": _has_explicit_row(source_n, k, DEFAULT_CSV),
            "base_typed": source is not None,
            "base_type": type(source).__name__ if source is not None else None,
            "base_group": group_coordinates(source) if source is not None else None,
            "base_admitted": admitted is not None,
            "target_count": len(goal_candidates),
            "proof_status": result.status.value,
            "diagnostics": list(result.diagnostics),
            "used_database_steps": [
                {"coordinates": group_coordinates(step.conclusion), "note": step.note}
                for step in result.proven_steps
                if (step.note or "").startswith("ADOPTED_DATABASE_PRIOR;")
            ],
        }
        print(f"R10E4R2_pi_{n+k}^{n}_BASE_ROW_PRESENT={item['base_row_present']}")
        print(f"R10E4R2_pi_{n+k}^{n}_BASE_TYPED={item['base_typed']}")
        print(f"R10E4R2_pi_{n+k}^{n}_BASE_ADMITTED={item['base_admitted']}")
        print(f"R10E4R2_pi_{n+k}^{n}_STATUS={item['proof_status']}")
        report.append(item)
    if not report[0]["base_typed"]:
        raise RuntimeError("R10E4R2 seven-stem stable base remains unavailable")
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps({"phase": "169 R10E4R2", "cases": report,
                    "full_pytest_run": False}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("R10E4R2_AUDIT=" + str(OUTPUT / "audit.json"))
    print("R10E4R2_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
