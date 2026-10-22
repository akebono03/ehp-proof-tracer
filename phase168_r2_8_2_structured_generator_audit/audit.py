"""Read-only structural comparison of the nine Phase 168 citation mismatches."""
from __future__ import annotations

from dataclasses import fields, is_dataclass
import json
from pathlib import Path

import pandas as pd

from phase168_r2_8_1_citation_mismatch_audit.audit import CASES, classify_relation
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import Relation
from unified_statement_registry import AssertionOrigin


def structure(value):
    """Serialize real expression dataclasses without inventing equivalences."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (tuple, list)):
        return [structure(item) for item in value]
    if is_dataclass(value) and not isinstance(value, type):
        result = {"type": type(value).__name__}
        for field in fields(value):
            result[field.name] = structure(getattr(value, field.name))
        if type(value).__name__ in {"HomotopyElement", "IteratedSuspension", "Suspension"}:
            result["effective_source"] = structure(getattr(value, "source", None))
            result["effective_target"] = structure(getattr(value, "target", None))
        if type(value).__name__ == "Composition":
            result["type_compatible"] = value.is_type_compatible()
        return result
    return {"type": type(value).__name__, "repr": repr(value)}


def differences(a, b, path="rhs"):
    """Report syntactic structural differences, not mathematical inequality."""
    if type(a) is not type(b):
        return [{"path": path, "left": a, "right": b}]
    if isinstance(a, dict):
        output = []
        for key in sorted(set(a) | set(b)):
            output += differences(a.get(key), b.get(key), path + "." + key)
        return output
    if isinstance(a, list):
        if len(a) != len(b):
            return [{"path": path + ".length", "left": len(a), "right": len(b)}]
        output = []
        for i, (left, right) in enumerate(zip(a, b)):
            output += differences(left, right, f"{path}[{i}]")
        return output
    return [] if a == b else [{"path": path, "left": a, "right": b}]


def db_rows(root, n, k):
    sphere = root / "data" / "sphere.csv"
    master = root / "data" / "HyoujiGen.csv"
    if not sphere.is_file() or not master.is_file():
        return {"status": "CSV_MISSING"}
    df = pd.read_csv(sphere)
    rows = df[(df["n"] == n) & (df["k"] == k)]
    selected = []
    for _, row in rows.iterrows():
        selected.append({name: None if pd.isna(row[name]) else str(row[name])
                         for name in ("id", "Element", "gen_coe", "generator", "orders")
                         if name in row.index})
    return {"status": "FOUND" if selected else "NO_ROWS", "rows": selected}


def inspect_case(bridge, root, n, k, locator):
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    db_goals = database_structured_group_goal_candidates(n=n, k=k)
    entry = {"n": n, "k": k, "locator": locator,
             "goal_count": len(goals), "db_goal_count": len(db_goals),
             "db_records": db_rows(root, n, k), "assertions": []}
    entry["goal"] = structure(goals[0]) if len(goals) == 1 else [structure(g) for g in goals]
    entry["db_goal"] = structure(db_goals[0]) if len(db_goals) == 1 else [structure(g) for g in db_goals]
    entry["goal_vs_db"] = differences(structure(goals[0]), structure(db_goals[0]), "relation") if len(goals) == len(db_goals) == 1 else None
    entry["resolved_id"] = resolve_specialized_goal_citing_id(bridge, goals[0]) if len(goals) == 1 else None
    if len(goals) != 1:
        entry["status"] = "GOAL_NOT_UNIQUE"
    else:
        entry["status"] = "RESOLVED" if entry["resolved_id"] else "UNRESOLVED"
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        if ref.locator != locator or not isinstance(assertion.content, Relation):
            continue
        content = assertion.content
        entry["assertions"].append({
            "id": assertion.assertion_id,
            "publication_position": ref.publication_position,
            "component_position": assertion.component_position,
            "classification": classify_relation(goals[0], content) if len(goals) == 1 else "NO_UNIQUE_GOAL",
            "relation": structure(content),
            "rhs_differences": differences(structure(goals[0].rhs), structure(content.rhs)) if len(goals) == 1 else None,
            "db_rhs_differences": differences(structure(db_goals[0].rhs), structure(content.rhs)) if len(db_goals) == 1 else None,
        })
    return entry


def main():
    root = Path(__file__).resolve().parent.parent
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, root, n, k, locator) for n, k, locator in CASES]
    report = {"audit": "phase168-r2-8-2", "read_only": True,
              "identity_certified": False, "production_code_modified": False, "cases": cases}
    output = Path(__file__).resolve().parent / "output" / "structured_comparison.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    for case in cases:
        print(f"pi_{case['n']+case['k']}^{case['n']}: {case['status']}, db_goals={case['db_goal_count']}, assertions={len(case['assertions'])}")
    print("REPORT:", output)


if __name__ == "__main__":
    main()
