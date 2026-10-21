"""R3-AH: inspect actual goal origin, publication binding, and failed subgoals."""
from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3af_goal_adapter import database_group_goal_candidates
from phase166_r3ag_actual_search_audit.audit import CASES, analyze_case
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import Relation
from unified_statement_registry import AssertionOrigin


def contained_relations(value: object) -> tuple[Relation, ...]:
    """Inspect real registered typed components, without creating statements."""
    output: list[Relation] = []
    seen: set[int] = set()

    def visit(obj: object) -> None:
        if id(obj) in seen:
            return
        seen.add(id(obj))
        if isinstance(obj, Relation):
            output.append(obj)
            return
        if is_dataclass(obj) and not isinstance(obj, type):
            for field in fields(obj):
                visit(getattr(obj, field.name))
        elif isinstance(obj, (tuple, list)):
            for part in obj:
                visit(part)

    visit(value)
    return tuple(output)


def assertion_matches(bridge, goal: Relation) -> list[dict]:
    """Separate literal fixed claims from any inferred/generic goal candidates."""
    matches = []
    for assertion in bridge.registry._assertions.values():
        relations = contained_relations(assertion.content)
        if not any(relation == goal for relation in relations):
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        matches.append({
            "assertion_id": assertion.assertion_id,
            "origin": str(assertion.origin),
            "reference_id": assertion.reference_id,
            "publication_position": repr(ref.publication_position),
            "component_position": assertion.component_position,
        })
    return matches


def inspect_case(bridge, k: int, n: int) -> dict:
    previous = analyze_case(bridge, k, n)
    registered = registered_group_goal_candidates(bridge, n=n, k=k)
    db = database_group_goal_candidates(n=n, k=k)
    selected = registered if registered else db
    record = {
        "stem": k, "n": n,
        "registered_count": len(registered), "database_count": len(db),
        "goal_sources_equal": len(registered) == len(db) == 1 and registered[0] == db[0],
        "registered_goals": [repr(x) for x in registered],
        "database_goals": [repr(x) for x in db],
        "open_goals": previous.get("open_goals", []),
        "diagnostics": previous.get("diagnostics", []),
        "search_status": previous.get("search_status"),
    }
    if len(selected) != 1:
        record["classification"] = "NO_UNIQUE_GOAL"
        return record
    goal = selected[0]
    record["exact_registry_matches"] = assertion_matches(bridge, goal)
    record["resolver_citing_id"] = resolve_specialized_goal_citing_id(bridge, goal)
    record["is_goal_an_existing_fixed_claim"] = any(
        x["origin"] == str(AssertionOrigin.FIXED_STATEMENT)
        for x in record["exact_registry_matches"]
    )
    record["base_group"] = repr(TodaPrimaryGroup(2 * k + 2, k + 2))
    base = TodaPrimaryGroup(2 * k + 2, k + 2)
    record["base_fixed_claims"] = []
    record["toda45_fixed_claims"] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        name = type(assertion.content).__name__
        if name == "Toda45IsomorphismStatement":
            record["toda45_fixed_claims"].append(assertion.assertion_id)
        if any(r.lhs == base for r in contained_relations(assertion.content)):
            record["base_fixed_claims"].append({"assertion_id": assertion.assertion_id,
                                                   "statement": repr(assertion.content)})
    if record["resolver_citing_id"] is None:
        record["classification"] = "NO_RESOLVED_PUBLICATION_BOUNDARY"
    else:
        record["classification"] = "PUBLICATION_BOUNDARY_RESOLVED"
    return record


def audit() -> dict:
    bridge = build_shared_typed_bridge()
    rows = [inspect_case(bridge, k, n) for k, n in CASES]
    return {"phase": "166 R3-AH", "production_modified": False, "cases": rows,
            "summary": {"cases": len(rows),
                        "unbound": sum(x["resolver_citing_id"] is None for x in rows),
                        "open_goal_total": sum(len(x["open_goals"]) for x in rows),
                        "exact_fixed_matches": sum(x["is_goal_an_existing_fixed_claim"] for x in rows)}}


def main() -> None:
    data = audit()
    report = Path(__file__).with_name("report.json")
    report.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"summary": data["summary"], "cases": [
        {"stem": x["stem"], "n": x["n"], "source_equal": x["goal_sources_equal"],
         "exact_registry_matches": x["exact_registry_matches"],
         "base_fixed_claim_ids": [v["assertion_id"] for v in x["base_fixed_claims"]],
         "toda45_fixed_claim_ids": x["toda45_fixed_claims"],
         "citing_id": x["resolver_citing_id"], "open_goals": x["open_goals"],
         "diagnostics": x["diagnostics"]} for x in data["cases"]],
         "report": str(report)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
