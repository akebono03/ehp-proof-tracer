"""R12-R25: read-only diagnostic of the actual Web proof-order execution path.

This module creates no ProofStep and changes no registry, rule, or Web route.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import PartialProofResult
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from proof import Relation


def describe(value: Any) -> dict[str, Any]:
    """Provide comparable typed fields without guessing mathematical equivalence."""
    if isinstance(value, Relation):
        return {"type": "Relation", "lhs": describe(value.lhs), "rhs": describe(value.rhs),
                "relation_type": str(value.relation_type)}
    if is_dataclass(value) and not isinstance(value, type):
        return {"type": type(value).__name__, "fields": {
            field.name: describe(getattr(value, field.name)) for field in fields(value)
        }}
    if isinstance(value, (tuple, list)):
        return {"type": type(value).__name__, "elements": [describe(item) for item in value]}
    if isinstance(value, (int, str, bool)) or value is None:
        return {"type": type(value).__name__, "value": value}
    return {"type": type(value).__name__, "repr": repr(value)}


def summarize_result(result: PartialProofResult) -> dict[str, Any]:
    return {"status": result.status.value, "conclusion": repr(result.conclusion),
            "proven_step_count": len(result.proven_steps),
            "open_goals": [repr(goal) for goal in result.open_goals],
            "diagnostics": list(result.diagnostics)}


def inspect_order(bridge, goal: Relation, *, n: int, k: int) -> dict[str, Any]:
    """Run the same resolver as the Web entry, then compare actual typed goals."""
    catalog, diagnostic = resolve_reviewed_order_catalog(bridge, n=n, k=k)
    records = tuple(getattr(catalog, "_records", ())) if catalog is not None else ()
    matches = tuple(record for record in records if type(record.statement) is type(goal)
                    and record.statement == goal)
    result = {"resolver_diagnostic": diagnostic, "catalog_available": catalog is not None,
              "catalog_target_count": len(records), "exact_goal_matches": len(matches),
              "web_goal": describe(goal), "registered_targets": [
                  {"position": record.position, "statement": describe(record.statement),
                   "exact_match": record.statement == goal} for record in records],
              "web_goal_repr": repr(goal)}
    if catalog is not None:
        try:
            prior, pos = catalog.select_prior(goal)
            result.update({"selection": "RESOLVED", "target_position": pos,
                           "completed_prior_count": len(prior)})
        except ValueError as exc:
            result.update({"selection": "FAILED", "selection_error": str(exc)})
    else:
        result["selection"] = "NOT_AVAILABLE"
    return result


def inspect_backward_candidates(bridge, goal: Relation) -> dict[str, Any]:
    """Inspect the actual common provider without asserting that proposals prove anything."""
    try:
        provider = shared_expansion_provider(bridge, proof_target=goal)
        first = tuple(provider(goal))
        subgoals = []
        for option in first:
            subgoals.extend(option.subgoals)
        return {"root_expansion_count": len(first),
                "root_rule_names": [getattr(option.rule, "name", type(option.rule).__name__) for option in first],
                "immediate_subgoals": [repr(item) for item in subgoals],
                "cyclic_structure_subgoal_count": sum(type(item).__name__ == "CyclicStructureStatement" for item in subgoals)}
    except (ValueError, TypeError, ImportError) as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def audit_web_order(*, n: int = 3, k: int = 1) -> dict[str, Any]:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    report: dict[str, Any] = {
        "phase": "165 R12-R25", "mode": "READ_ONLY_WEB_PROOF_ORDER_DIAGNOSTIC",
        "target": repr(TodaPrimaryGroup(n+k, n)), "candidate_count": len(goals),
        "candidates": [describe(candidate) for candidate in goals],
        "registered_assertion_count": len(bridge.registry._assertions),
        "fixed_link_count": len(bridge.proof_links),
        "full_pytest_run": False,
        "no_proofstep_injected": True, "no_web_override": True,
    }
    if len(goals) == 1:
        goal = goals[0]
        report["order"] = inspect_order(bridge, goal, n=n, k=k)
        report["backward"] = inspect_backward_candidates(bridge, goal)
    else:
        report["order"] = {"selection": "CANDIDATE_NOT_UNIQUE"}
        report["backward"] = {"root_expansion_count": None}
    try:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        report["canonical_result"] = summarize_result(result)
    except Exception as exc:
        report["canonical_error"] = f"{type(exc).__name__}: {exc}"
    try:
        view = build_group_proof_progress_view(n=n, k=k)
        report["web_view"] = {"key": view.key, "partial_result": view.partial_result,
                              "step_count": len(view.steps), "rendered_line_count": len(view.rendered_lines)}
    except Exception as exc:
        report["web_error"] = f"{type(exc).__name__}: {exc}"
    selection = report["order"].get("selection")
    report["status"] = "DIAGNOSED_ORDER_MISMATCH" if selection == "FAILED" else (
        "ORDER_RESOLVED_SEARCH_REVIEW" if selection == "RESOLVED" else "ORDER_OR_GOAL_SELECTION_REVIEW")
    return report
