from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from proof import (
    ProofRule,
    Relation,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from repository_proof_scope import build_repository_proof_scope
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from standard_production_repository import build_standard_production_proof_repository
from toda_rules import TodaProp42ExactnessStatement, TodaProp51FiniteDimensionalStatement


OUTPUT_NAME = "phase161_backward_type_closure_probe.json"
MAX_TYPE_DEPTH = 4
MAX_EXECUTION_ROUNDS = 7
MAX_GENERATED_STEPS = 80
MAX_CANDIDATE_RULES = 1000


def unique_steps(steps):
    found = set()
    result = []
    for step in steps:
        key = id(step)
        if key not in found:
            found.add(key)
            result.append(step)
    return tuple(result)


def goal_and_exactness():
    group = lambda dimension, sphere: TodaPrimaryGroup(
        group_dimension=dimension, sphere_dimension=sphere
    )
    pi42, pi53, pi55 = group(4, 2), group(5, 3), group(5, 5)
    pi32, pi63, pi65 = group(3, 2), group(6, 3), group(6, 5)
    goal = TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(source_group=pi42, target_group=pi53)
    )
    windows = (
        (pi53, pi55, pi32, EHP_H_MAP, EHP_DELTA_MAP),
        (pi42, pi53, pi55, EHP_E_MAP, EHP_H_MAP),
        (pi63, pi65, pi42, EHP_H_MAP, EHP_DELTA_MAP),
        (pi65, pi42, pi53, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        TodaProp42ExactnessStatement(
            window=TodaEHPExactnessWindow(
                source_term=a,
                middle_term=b,
                target_term=c,
                first_map=first,
                second_map=second,
            )
        )
        for a, b, c, first, second in windows
    )
    return goal, exactness


def backward_type_closure(entries, goal_type, max_depth):
    levels = []
    known = {goal_type}
    frontier = {goal_type}
    for depth in range(max_depth + 1):
        candidate_entries = [
            entry for entry in entries if entry.conclusion_type in frontier
        ]
        new_types = set()
        for entry in candidate_entries:
            for pattern in entry.rule.premise_patterns:
                if pattern.statement_type is not None:
                    new_types.add(pattern.statement_type)
                elif pattern.relation_type is not None:
                    new_types.add(Relation)
        levels.append({
            "depth": depth,
            "frontier_types": sorted(cls.__name__ for cls in frontier),
            "candidate_entries": len(candidate_entries),
            "new_premise_types": sorted(cls.__name__ for cls in new_types),
        })
        frontier = new_types - known
        known.update(new_types)
        if not frontier:
            break
    return known, levels


def find_initial_facts(steps, exactness):
    windows = [
        tuple(
            step for step in steps
            if step.conclusion == statement and step.rule is ProofRule.GIVEN
        )
        for statement in exactness
    ]
    proposition_steps = unique_steps(
        step for step in steps
        if isinstance(step.conclusion, TodaProp51FiniteDimensionalStatement)
        and step.rule is ProofRule.INFERENCE
    )
    relation_steps = unique_steps(
        step for step in steps
        if isinstance(step.conclusion, Relation)
        and step.rule is ProofRule.INFERENCE
        and step.inference_rule is not None
        and step.inference_rule.name == "equality transitivity"
    )
    return windows, proposition_steps, relation_steps


def execute_restricted_forward_chain(entries, initial_steps, goal, relevant_types):
    available = list(initial_steps)
    initial_ids = {id(step) for step in initial_steps}
    existing_conclusions = [step.conclusion for step in available]
    diagnostics = []
    usable = [
        entry for entry in entries
        if entry.conclusion_type in relevant_types
        and (entry.rule.conclusion_builder is not None or entry.rule.conclusion_pattern is not None)
    ]
    if len(usable) > MAX_CANDIDATE_RULES:
        return False, diagnostics, "CANDIDATE_BUDGET", len(usable)
    for round_number in range(1, MAX_EXECUTION_ROUNDS + 1):
        added = []
        attempted_rules = 0
        applicable_rules = 0
        error_count = 0
        for entry in usable:
            attempted_rules += 1
            try:
                matches = find_inference_matches_for_rule(entry.rule, tuple(available))
            except (ValueError, TypeError, RuntimeError):
                error_count += 1
                continue
            if matches:
                applicable_rules += 1
            for match in matches:
                try:
                    new_step = apply_inference_match(match)
                except (ValueError, TypeError, RuntimeError):
                    error_count += 1
                    continue
                if any(new_step.conclusion == item for item in existing_conclusions):
                    continue
                if any(new_step.conclusion == item.conclusion for item in added):
                    continue
                added.append(new_step)
                if len(available) + len(added) - len(initial_steps) >= MAX_GENERATED_STEPS:
                    return False, diagnostics, "STEP_BUDGET", len(usable)
        for step in added:
            available.append(step)
            existing_conclusions.append(step.conclusion)
        goal_step = next((step for step in available if step.conclusion == goal), None)
        diagnostics.append({
            "round": round_number,
            "candidate_rules": attempted_rules,
            "applicable_rules": applicable_rules,
            "errors": error_count,
            "new_steps": len(added),
            "new_statement_types": sorted({type(step.conclusion).__name__ for step in added}),
            "goal_found": goal_step is not None,
        })
        if goal_step is not None:
            # Count recursively reachable new inference nodes; no synthetic facts.
            seen = set()
            def trace(step):
                if id(step) in seen:
                    return []
                seen.add(id(step))
                items = []
                for premise in step.premises:
                    if hasattr(premise, "conclusion"):
                        items.extend(trace(premise))
                if id(step) not in initial_ids:
                    items.append({
                        "type": type(step.conclusion).__name__,
                        "rule_name_for_reporting": step.inference_rule.name if step.inference_rule else None,
                        "proof_rule": step.rule.name,
                    })
                return items
            return True, {"rounds": diagnostics, "proof_nodes": trace(goal_step)}, "GOAL_DERIVED", len(usable)
        if not added:
            break
    return False, diagnostics, "NO_DERIVATION_WITHIN_LIMITS", len(usable)


def main():
    repository = build_standard_production_proof_repository()
    scope = build_repository_proof_scope(repository)
    catalog = build_standard_production_applicability_catalog()
    steps = unique_steps(node.proof_step for node in scope.nodes)
    goal, exactness = goal_and_exactness()
    entries = catalog.entries()
    types, levels = backward_type_closure(entries, type(goal), MAX_TYPE_DEPTH)
    windows, propositions, relations = find_initial_facts(steps, exactness)
    output = {
        "scope": "Goal-only backward STATEMENT-TYPE closure and bounded forward proof execution using a six-premise semantic seed profile; not full concrete backward chaining",
        "input_goal": repr(goal),
        "intermediate_goals_prelisted": False,
        "rule_family_names_prelisted": False,
        "six_premise_profile_still_preselected": True,
        "relation_provenance_name_filter_still_used": True,
        "type_depth_limit": MAX_TYPE_DEPTH,
        "type_levels": levels,
        "type_closure_size": len(types),
        "production_scope_nodes": len(scope.nodes),
        "production_catalog_entries": len(entries),
        "four_exactness_candidate_counts": [len(group) for group in windows],
        "proposition_candidates": len(propositions),
        "relation_candidates": len(relations),
        "success": False,
        "pairs_attempted": 0,
    }
    if not all(windows) or not propositions or not relations:
        output["status"] = "MISSING_SEED_FACTS"
        return output
    baseline = tuple(group[0] for group in windows)
    candidate_details = []
    for prop in propositions:
        for relation in relations:
            output["pairs_attempted"] += 1
            initial = (prop, relation) + baseline
            succeeded, details, status, count = execute_restricted_forward_chain(
                entries, initial, goal, types
            )
            if len(candidate_details) < 3:
                candidate_details.append({"status": status, "details": details})
            if succeeded:
                output.update({
                    "success": True,
                    "status": "TYPE_BACKWARD_CLOSURE_AND_REAL_EXECUTION_SUCCESS",
                    "selected_candidate_rule_count": count,
                    "execution": details,
                    "initial_provenance": [
                        {"statement_type": type(step.conclusion).__name__,
                         "proof_rule": step.rule.name,
                         "inference_name_for_reporting": step.inference_rule.name if step.inference_rule else None}
                        for step in initial
                    ],
                })
                return output
            if output["pairs_attempted"] >= 5:
                break
        if output["pairs_attempted"] >= 5:
            break
    output["status"] = "NOT_PROVEN_WITHIN_BOUNDED_HYBRID_SEARCH"
    output["first_attempts"] = candidate_details
    return output


if __name__ == "__main__":
    outcome = main()
    print(json.dumps(outcome, indent=2, ensure_ascii=False))
    destination = Path(OUTPUT_NAME)
    destination.write_text(json.dumps(outcome, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote:", destination.resolve())
    if not outcome["success"]:
        raise SystemExit(1)
