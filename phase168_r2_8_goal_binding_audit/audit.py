"""Phase 168 R2-8: read-only goal / citation boundary audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import ProofRule, Relation
from toda_literature_statement_boundary import TodaFixedStatementComponent

CASES = (
    (2, 1, "Proposition 5.1"),
    (3, 1, "Proposition 5.1"),
    (4, 1, "Proposition 5.1"),
    (2, 2, "Proposition 5.3"),
    (3, 2, "Proposition 5.3"),
    (4, 2, "Proposition 5.3"),
    (5, 2, "Proposition 5.3"),
    (2, 3, "Proposition 5.6"),
    (3, 3, "Proposition 5.6"),
    (4, 3, "Proposition 5.6"),
    (5, 3, "Proposition 5.6"),
    (6, 3, "Proposition 5.6"),
)

def audit_case(bridge, n: int, k: int, expected_locator: str) -> dict:
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    result = {
        "n": n, "k": k, "group": f"pi_{n+k}^{n}",
        "expected_locator": expected_locator,
        "goal_count": len(goals),
        "goals": [repr(g) for g in goals],
        "citing_assertion_id": None,
        "actual_locator": None,
        "citing_position": None,
        "generated_given_count": None,
        "self_conclusion_generated": None,
        "metadata_given_count": None,
        "wrong_locator": None,
        "status": None,
    }
    if len(goals) != 1:
        result["status"] = "GOAL_NOT_UNIQUE"
        return result
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    result["citing_assertion_id"] = citing_id
    if citing_id is None:
        result["status"] = "CITING_ID_UNRESOLVED"
        return result
    assertion = bridge.registry.assertion(citing_id)
    reference = bridge.registry.reference(assertion.reference_id)
    result["actual_locator"] = reference.locator
    result["citing_position"] = [reference.publication_position, assertion.component_position]
    result["wrong_locator"] = reference.locator != expected_locator
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    given = tuple(link for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN)
    result["generated_given_count"] = len(given)
    result["self_conclusion_generated"] = any(link.step.conclusion == goal for link in given)
    result["metadata_given_count"] = sum(
        isinstance(bridge.registry.assertion(link.assertion_id).content,
                   TodaFixedStatementComponent) for link in given
    )
    result["status"] = (
        "WRONG_LOCATOR" if result["wrong_locator"] else
        "SELF_CONCLUSION" if result["self_conclusion_generated"] else
        "METADATA_GIVEN" if result["metadata_given_count"] else
        "OK"
    )
    return result

def run_audit() -> dict:
    bridge = build_shared_typed_bridge()
    rows = [audit_case(bridge, n, k, loc) for n, k, loc in CASES]
    return {
        "audit": "phase168-r2-8-goal-binding",
        "production_code_modified": False,
        "cases": rows,
        "status_counts": {status: sum(row["status"] == status for row in rows)
                          for status in sorted({row["status"] for row in rows})},
    }

def main() -> None:
    report = run_audit()
    target = Path(__file__).resolve().parent / "output" / "goal_binding_audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    for row in report["cases"]:
        print(f"{row['group']:9} {row['status']:21} "
              f"citing={row['citing_assertion_id']}")
    print("SUMMARY", json.dumps(report["status_counts"], ensure_ascii=False))
    print("JSON:", target)
    # The audit is observational: unresolved cases are recorded, not patched.

if __name__ == "__main__":
    main()
