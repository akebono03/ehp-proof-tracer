"""Read-only inspection of the source provenance of the pi_4^3 proof."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import ordered_proof_ancestry
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule


def audit() -> dict:
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    roots = [step for step in result.proven_steps if step.conclusion == result.conclusion and step.rule is ProofRule.INFERENCE]
    if len(roots) != 1:
        raise ValueError(f"Expected one root, found {len(roots)}")
    steps = ordered_proof_ancestry(roots[0])
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assertions = tuple(bridge.registry._assertions.values())
    proof_links = tuple(bridge.proof_links)
    rows = []
    from phase166_r3c_publication_order import precedes_citing_assertion
    for number, step in enumerate(steps, 1):
        if step.rule is not ProofRule.GIVEN:
            continue
        reference = getattr(step.inference_rule, "literature_reference", None)
        locator = getattr(reference, "locator", None)
        matches = []
        for assertion in assertions:
            if assertion.content != step.conclusion:
                continue
            ref = bridge.registry.reference(assertion.reference_id)
            matching_links = tuple(link for link in proof_links if link.assertion_id == assertion.assertion_id)
            matches.append({
                "assertion_id": assertion.assertion_id,
                "reference_id": assertion.reference_id,
                "origin": assertion.origin.value,
                "publication_position": ref.publication_position,
                "component_position": assertion.component_position,
                "linked_in_bridge": bool(matching_links),
                "link_count": len(matching_links),
                "precedes_actual_citing_id": (
                    precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)
                    if citing_id is not None else None
                ),
            })
        rows.append({
            "step": number,
            "locator": locator,
            "conclusion_type": type(step.conclusion).__name__,
            "matched_assertions": matches,
            "matched_count": len(matches),
            "status": "NOT_MAPPED" if not matches else (
                "MULTIPLE_MATCHES" if len(matches) > 1 else "MAPPED_NO_CITING_ID" if citing_id is None else
                "VERIFIED" if matches[0]["precedes_actual_citing_id"] else "NOT_PRECEDING"
            ),
        })
    report = {
        "phase": "167 R3",
        "mode": "READ_ONLY_GIVEN_ASSERTION_PROVENANCE",
        "search_status": result.status.value,
        "total_steps": len(steps),
        "given_count": len(rows),
        "citing_id": citing_id,
        "citing_id_policy": "The production citing ID is not invented when resolver returns None.",
        "given_assertions": rows,
        "publication_order_verified": len(rows) > 0 and all(row["status"] == "VERIFIED" for row in rows),
        "limitation": "Provenance mapping and relative metadata are inspected; no synthetic target position is assigned. A missing citing ID cannot certify publication order.",
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    path = Path(__file__).with_name("r3_publication_provenance_report.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    result = audit()
    print(json.dumps({
        "search_status": result["search_status"],
        "total_steps": result["total_steps"],
        "given_count": result["given_count"],
        "citing_id": result["citing_id"],
        "given_checks": [{"step": r["step"], "locator": r["locator"], "matched_count": r["matched_count"], "status": r["status"]} for r in result["given_assertions"]],
        "publication_order_verified": result["publication_order_verified"],
        "report": str(Path(__file__).with_name("r3_publication_provenance_report.json")),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
