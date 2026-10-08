from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from proof import (
    apply_inference_match,
    find_inference_matches_for_rule,
    match_statement_pattern,
)
from repository_proof_scope import build_repository_proof_scope
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from standard_production_repository import build_standard_production_proof_repository


OUTPUT = "phase161_concrete_goal_filter_audit.json"


def make_goal():
    return TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )


def unique_steps(steps):
    seen = set()
    result = []
    for step in steps:
        if id(step) not in seen:
            seen.add(id(step))
            result.append(step)
    return tuple(result)


def inspect_concrete_goal(entries, goal, available_steps):
    result = {
        "goal": repr(goal),
        "type_candidate_count": 0,
        "invertible_pattern_count": 0,
        "pattern_exact_count": 0,
        "pattern_incompatible_count": 0,
        "builder_only_count": 0,
        "non_executable_count": 0,
        "actual_match_count": 0,
        "exact_output_count": 0,
        "exact_producer_keys": [],
        "builder_only_keys": [],
        "errors": [],
    }
    for entry in entries:
        if entry.conclusion_type is not type(goal):
            continue
        result["type_candidate_count"] += 1
        rule = entry.rule
        if rule.conclusion_pattern is not None:
            result["invertible_pattern_count"] += 1
            try:
                bindings = match_statement_pattern(rule.conclusion_pattern, goal)
            except (TypeError, ValueError) as error:
                result["errors"].append({"key": entry.key, "error": str(error)})
                continue
            if bindings is None:
                result["pattern_incompatible_count"] += 1
                continue
            result["pattern_exact_count"] += 1
        elif rule.conclusion_builder is not None:
            result["builder_only_count"] += 1
            result["builder_only_keys"].append(entry.key)
        else:
            result["non_executable_count"] += 1
            continue
        # This stage validates concrete conclusions from REAL steps only.
        # Existing proof-scope steps are witness data, NOT independent proof discovery.
        try:
            matches = find_inference_matches_for_rule(rule, available_steps)
        except (TypeError, ValueError, RuntimeError) as error:
            result["errors"].append({"key": entry.key, "error": str(error)})
            continue
        result["actual_match_count"] += len(matches)
        matched = False
        for match in matches:
            try:
                inferred = apply_inference_match(match)
            except (TypeError, ValueError, RuntimeError) as error:
                result["errors"].append({"key": entry.key, "error": str(error)})
                continue
            if inferred.conclusion == goal:
                result["exact_output_count"] += 1
                matched = True
        if matched:
            result["exact_producer_keys"].append(entry.key)
    result["concrete_goal_filter_usable_without_premises"] = result["pattern_exact_count"]
    result["builder_only_needs_forward_witness"] = result["builder_only_count"]
    return result


def main():
    repo = build_standard_production_proof_repository()
    scope = build_repository_proof_scope(repo)
    catalog = build_standard_production_applicability_catalog()
    goal = make_goal()
    # Diagnostic witness collection, NOT a seed set for proof execution.
    witnesses = unique_steps(node.proof_step for node in scope.nodes)
    result = {
        "purpose": "Concrete-goal matching capability audit. No per-type beam, no fabricated ProofStep; NOT a completed goal-only proof search.",
        "goal_only_input": repr(goal),
        "scope_node_count": len(scope.nodes),
        "witness_step_count": len(witnesses),
        "catalog_entry_count": len(catalog.entries()),
        "uses_existing_target_ancestry_as_witness": True,
        "uses_witnesses_for_new_proof": False,
        "audit": inspect_concrete_goal(catalog.entries(), goal, witnesses),
    }
    if result["audit"]["builder_only_count"]:
        result["status"] = "CONCRETE_BACKWARD_METADATA_GAP_CONFIRMED"
    else:
        result["status"] = "CONCRETE_PATTERN_COVERAGE_RECORDED"
    return result


if __name__ == "__main__":
    result = main()
    output = Path(OUTPUT)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Wrote:", output.resolve())
