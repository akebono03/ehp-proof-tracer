"""Focused R10EG audit: observed complete Proof Trees and source replay only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary.verification import verify_proof_tree_for_narrative
from proof import ProofRule

CASES = ((2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (30, 1),
         (8, 2), (15, 8), (13, 9), (24, 9))


def inspect_case(bridge: object, n: int, k: int) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    row = {
        "group": f"pi_{n+k}^{n}",
        "n": n, "k": k,
        "status": result.status.value,
        "open_goals": [type(x).__name__ for x in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "proof_steps": len(result.proven_steps),
        "inferred_root_steps": 0,
        "trust": "NOT_APPLICABLE_INCOMPLETE",
    }
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        return row
    row["inferred_root_steps"] = sum(
        item.rule is ProofRule.INFERENCE and item.conclusion == result.conclusion
        for item in result.proven_steps
    )
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[-1], citing_assertion_id=citing_id,
        derived_target_without_citing_id=citing_id is None,
    )
    row.update(trust="PASS", inference_count=inferred, given_count=given,
               citations_present=given > 0)
    return row


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: audit.py OUTPUT_DIRECTORY")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, n, k) for n, k in CASES]
    for row in cases:
        key = "R10EG_" + row["group"]
        print(key + "_STATUS=" + row["status"], flush=True)
        print(key + "_TRUST=" + row["trust"], flush=True)
        print(key + "_PROOF_STEPS=" + str(row["proof_steps"]), flush=True)
        if row["diagnostics"]:
            print(key + "_DIAGNOSTICS=" + json.dumps(row["diagnostics"], ensure_ascii=False), flush=True)
    report = {"phase": "169 R10EG", "mode": "FOCUSED_REGRESSION",
              "cases": cases, "inference_rules_changed": False,
              "source_registry_changed": False, "full_pytest_run": False}
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("R10EG_AUDIT_JSON=" + str(output / "audit.json"))
    if not all(x["status"] == "complete" and x["trust"] == "PASS"
               and x["inferred_root_steps"] == 1 for x in cases):
        raise RuntimeError("R10EG complete-proof or uniqueness regression")
    if cases[2]["proof_steps"] != 10:
        raise RuntimeError("R10EG frozen pi_5^4 proof step count not restored")
    print("R10EG_ALL_CASES_VERIFIED=PASS")
    print("R10EG_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
