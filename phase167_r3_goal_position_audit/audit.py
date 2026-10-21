from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from phase165_prop51_claim_order import pi4_3_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule

OUTPUT = Path(__file__).resolve().parent / "r3_goal_position_report.json"


def contains_statement(container: object, statement: object, seen: set[int] | None = None) -> bool:
    if container == statement:
        return True
    if seen is None:
        seen = set()
    if id(container) in seen:
        return False
    seen.add(id(container))
    if is_dataclass(container) and not isinstance(container, type):
        return any(contains_statement(getattr(container, field.name), statement, seen) for field in fields(container))
    if isinstance(container, (tuple, list)):
        return any(contains_statement(item, statement, seen) for item in container)
    return False


def main() -> None:
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1)
    expected = pi4_3_goal()
    goal = result.conclusion
    if goal is None:
        raise RuntimeError("The canonical pi_4^3 search did not return a conclusion")
    candidates = []
    for assertion in bridge.registry._assertions.values():
        exact = assertion.content == goal
        nested = contains_statement(assertion.content, goal)
        if not nested:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        candidates.append({
            "assertion_id": assertion.assertion_id,
            "reference_id": assertion.reference_id,
            "origin": assertion.origin.value,
            "publication_position": reference.publication_position,
            "component_position": assertion.component_position,
            "exact": exact,
            "nested": nested,
        })
    # A composite parent is not interchangeable with a specifically indexed
    # component. Do not choose one automatically if several positions exist.
    exact_candidates = [item for item in candidates if item["exact"]]
    usable = [item for item in exact_candidates if item["publication_position"] is not None
              and item["component_position"] is not None]
    resolved = usable[0]["assertion_id"] if len(usable) == 1 else None
    used_givens = [step for step in result.proven_steps if step.rule is ProofRule.GIVEN]
    given_results = []
    for step in used_givens:
        matches = []
        for assertion in bridge.registry._assertions.values():
            if assertion.content != step.conclusion:
                continue
            source = bridge.registry.reference(assertion.reference_id)
            matches.append({
                "assertion_id": assertion.assertion_id,
                "publication_position": source.publication_position,
                "component_position": assertion.component_position,
                "precedes_goal": precedes_citing_assertion(bridge, assertion.assertion_id, resolved)
                if resolved is not None else None,
            })
        given_results.append({
            "conclusion_type": type(step.conclusion).__name__,
            "locator": getattr(getattr(step.inference_rule, "literature_reference", None), "locator", None),
            "is_goal_itself": step.conclusion == goal,
            "matching_assertions": matches,
            "all_matches_precede": bool(matches) and all(item["precedes_goal"] is True for item in matches),
            "some_match_precedes": any(item["precedes_goal"] is True for item in matches),
        })
    output = {
        "phase": "167 R3 goal position audit",
        "mode": "READ_ONLY",
        "search_status": result.status.value,
        "goal_matches_declared_prop51_item": goal == expected,
        "production_citing_id": resolve_specialized_goal_citing_id(bridge, goal),
        "goal_assertion_candidates": candidates,
        "exact_candidate_count": len(exact_candidates),
        "usable_exact_candidate_count": len(usable),
        "unique_exact_citing_id": resolved,
        "given_count": len(given_results),
        "goal_used_as_given": any(item["is_goal_itself"] for item in given_results),
        "given_results": given_results,
        "publication_order_verified": resolved is not None and bool(given_results)
        and all(item["some_match_precedes"] for item in given_results),
        "warning": "A parent assertion's position must not be treated as the position of its unregistered component. The audit does not modify production search.",
        "full_pytest_run": False,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: output[k] for k in (
        "search_status", "goal_matches_declared_prop51_item", "production_citing_id",
        "exact_candidate_count", "usable_exact_candidate_count", "unique_exact_citing_id",
        "given_count", "goal_used_as_given", "publication_order_verified")}, ensure_ascii=False, indent=2))
    print("REPORT:", OUTPUT)


if __name__ == "__main__":
    main()
