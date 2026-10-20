"""Read-only comparison of implicit and publication-order proof premises."""
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass, fields, is_dataclass

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, Relation
from unified_statement_registry import AssertionOrigin

OUTPUT = Path("phase166_r3q_premise_comparison_results")
TARGETS = ((2, 1), (3, 1), (4, 1))


def contains_relation(content: object, goal: Relation) -> bool:
    if isinstance(content, Relation):
        return content == goal
    if is_dataclass(content) and not isinstance(content, type):
        for field in fields(content):
            val = getattr(content, field.name)
            if isinstance(val, (tuple, list)):
                if any(contains_relation(item, goal) for item in val):
                    return True
            elif is_dataclass(val) and not isinstance(val, type):
                if contains_relation(val, goal):
                    return True
    return False


def ordered_given_ids(bridge, goal, citing_id):
    context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    return {
        link.assertion_id for link in context.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    }


def implicit_given_ids(bridge, goal):
    first_id = next(iter(bridge.registry._assertions))
    context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=first_id,
        explicit_publication_target=False,
    )
    return {
        link.assertion_id for link in context.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    }


def describe(bridge, assertion_id):
    a = bridge.registry.assertion(assertion_id)
    ref = bridge.registry.reference(a.reference_id)
    return {
        "assertion_id": assertion_id,
        "reference_id": a.reference_id,
        "locator": ref.locator,
        "publication_position": ref.publication_position,
        "component_position": a.component_position,
        "origin": a.origin.value,
        "content_type": type(a.content).__name__,
    }


def inspect():
    bridge = build_shared_typed_bridge()
    results = []
    for n, k in TARGETS:
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        goal_records = []
        for goal in goals:
            matches = [
                assertion for assertion in bridge.registry._assertions.values()
                if assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and contains_relation(assertion.content, goal)
            ]
            implicit = implicit_given_ids(bridge, goal)
            boundaries = []
            for candidate in matches:
                ref = bridge.registry.reference(candidate.reference_id)
                if ref.publication_position is None or candidate.component_position is None:
                    boundary_status = "incomplete_position"
                else:
                    boundary_status = "positioned"
                explicit = ordered_given_ids(bridge, goal, candidate.assertion_id)
                missing = sorted(implicit - explicit)
                added = sorted(explicit - implicit)
                boundaries.append({
                    "boundary": describe(bridge, candidate.assertion_id),
                    "boundary_status": boundary_status,
                    "implicit_count": len(implicit),
                    "ordered_count": len(explicit),
                    "removed_from_implicit": [describe(bridge, x) for x in missing],
                    "added_by_ordered_mode": [describe(bridge, x) for x in added],
                    "prior_by_order_position": [
                        describe(bridge, a.assertion_id)
                        for a in bridge.registry._assertions.values()
                        if a.origin is AssertionOrigin.FIXED_STATEMENT
                        and precedes_citing_assertion(bridge, a.assertion_id, candidate.assertion_id)
                    ],
                })
            goal_records.append({
                "goal_repr": repr(goal),
                "matching_assertion_count": len(matches),
                "implicit_given_count": len(implicit),
                "matching_assertions": [describe(bridge, x.assertion_id) for x in matches],
                "comparisons": boundaries,
            })
        results.append({
            "n": n,
            "k": k,
            "registered_goal_count": len(goals),
            "goals": goal_records,
        })
    return {
        "audit": "phase166-r3q-premise-comparison",
        "production_code_modified": False,
        "full_pytest_run": False,
        "targets": results,
    }


def main():
    data = inspect()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    filename = OUTPUT / "audit.json"
    filename.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "audit": data["audit"],
        "production_code_modified": False,
        "targets": [
            {
                "n": item["n"], "k": item["k"],
                "registered_goal_count": item["registered_goal_count"],
                "comparison_count": sum(len(g["comparisons"]) for g in item["goals"]),
            }
            for item in data["targets"]
        ],
        "report": str(filename.resolve()),
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
