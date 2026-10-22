"""Read-only diagnosis of unresolved literature citation boundaries."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import Relation
from unified_statement_registry import AssertionOrigin

CASES = (
    (2, 2, "Proposition 5.3"), (3, 2, "Proposition 5.3"),
    (4, 2, "Proposition 5.3"), (5, 2, "Proposition 5.3"),
    (2, 3, "Proposition 5.6"), (3, 3, "Proposition 5.6"),
    (4, 3, "Proposition 5.6"), (5, 3, "Proposition 5.6"),
    (6, 3, "Proposition 5.6"),
)

def classify_relation(goal, statement):
    if not isinstance(statement, Relation):
        return "NOT_RELATION"
    if statement.lhs != goal.lhs:
        return "DIFFERENT_GROUP"
    if type(statement.rhs) is not type(goal.rhs):
        return "GROUP_STRUCTURE_TYPE_DIFFERENT"
    if statement.rhs == goal.rhs:
        return "EXACT_MATCH"
    if getattr(statement.rhs, "order", None) != getattr(goal.rhs, "order", None):
        return "ORDER_DIFFERENT"
    return "GENERATOR_OR_PRESENTATION_DIFFERENT"

def examine(bridge, n, k, locator):
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    row = {"n": n, "k": k, "expected_locator": locator, "goal_count": len(goals)}
    if len(goals) != 1:
        row["status"] = "GOAL_NOT_UNIQUE"
        return row
    goal = goals[0]
    row["goal"] = repr(goal)
    row["resolved_id"] = resolve_specialized_goal_citing_id(bridge, goal)
    row["references"] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        if ref.locator != locator:
            continue
        content = assertion.content
        if not isinstance(content, Relation):
            continue
        relation_class = classify_relation(goal, content)
        row["references"].append({
            "id": assertion.assertion_id,
            "class": relation_class,
            "position": ref.publication_position,
            "component_position": assertion.component_position,
            "content": repr(content),
        })
    row["match_classes"] = {name: sum(item["class"] == name for item in row["references"])
                            for name in sorted({item["class"] for item in row["references"]})}
    row["status"] = "RESOLVED" if row["resolved_id"] else "UNRESOLVED"
    return row

def main():
    bridge = build_shared_typed_bridge()
    rows = [examine(bridge, n, k, locator) for n, k, locator in CASES]
    result = {"audit": "phase168-r2-8-1", "production_code_modified": False, "cases": rows}
    output = Path(__file__).parent / "output" / "citation_mismatch.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"pi_{row['n']+row['k']}^{row['n']}: {row['status']} matches={row.get('match_classes', {})}")
    print("JSON:", output)

if __name__ == "__main__":
    main()
