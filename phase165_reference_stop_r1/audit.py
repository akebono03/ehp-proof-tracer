"""Read-only eligibility and stopping-boundary audit for pi_4^3."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def inspect_boundary() -> dict:
    bridge = build_shared_typed_bridge()
    pi32 = TodaPrimaryGroup(3, 2)
    pi43 = TodaPrimaryGroup(4, 3)
    candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    prior = registered_group_goal_candidates(bridge, n=2, k=1)
    order_catalog, order_diagnostic = resolve_reviewed_order_catalog(bridge, n=3, k=1)
    rows = []
    for assertion in bridge.registry._assertions.values():
        content = assertion.content
        if isinstance(content, Relation) and content.relation_type is RelationType.EQUALITY and content.lhs in (pi32, pi43):
            links = [link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id]
            rows.append({
                "assertion_id": assertion.assertion_id,
                "group": "pi32" if content.lhs == pi32 else "pi43",
                "origin": assertion.origin.value if hasattr(assertion.origin, "value") else str(assertion.origin),
                "content": repr(content),
                "proof_link_count": len(links),
                "matching_given_count": sum(
                    link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and link.step.conclusion == content
                    for link in links
                ),
                "reference_ids": [str(getattr(link, "assertion_id", "")) for link in links],
            })
    return {
        "phase": "165 reference-stop R1",
        "status": "ELIGIBILITY_BOUNDARY_INSPECTED_NO_SEARCH_PATCH",
        "pi43_goal_candidates": [repr(x) for x in candidates],
        "pi32_goal_candidates": [repr(x) for x in prior],
        "reviewed_order_catalog_available": order_catalog is not None,
        "order_diagnostic": order_diagnostic,
        "matching_registry_assertions": rows,
        "pi32_fixed_given_available": any(
            x["group"] == "pi32" and x["origin"] == AssertionOrigin.FIXED_STATEMENT.value
            and x["matching_given_count"] > 0 for x in rows
        ),
        "prior_internal_proof_eligible_for_search": "NOT_INSPECTED",
        "actual_pi43_proof_tree_checked": False,
        "search_stopping_behavior_verified": False,
        "source_files_modified": False,
        "full_pytest_run": False,
    }


def main() -> None:
    report = inspect_boundary()
    path = Path(__file__).resolve().parent / "audit_result.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", path)


if __name__ == "__main__":
    main()
