from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import (
    TodaDeltaMap,
    TodaHopfInvariantMap,
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
from standard_production_repository import build_standard_production_proof_repository
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaHopfInvariantZeroStatement,
    TodaProp42ExactnessStatement,
    TodaProp51FiniteDimensionalStatement,
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def unique_by_identity(steps):
    result = []
    seen = set()
    for step in steps:
        if id(step) not in seen:
            seen.add(id(step))
            result.append(step)
    return tuple(result)


def build_goals():
    g = lambda d, n: TodaPrimaryGroup(group_dimension=d, sphere_dimension=n)
    pi42, pi53, pi55 = g(4, 2), g(5, 3), g(5, 5)
    pi32, pi63, pi65 = g(3, 2), g(6, 3), g(6, 5)
    suspension = TodaSuspensionMap(source_group=pi42, target_group=pi53)
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
    goal_chain = (
        ("delta_injective", TodaDeltaInjectiveStatement(map=TodaDeltaMap(source_group=pi55, target_group=pi32))),
        ("hopf_zero", TodaHopfInvariantZeroStatement(map=TodaHopfInvariantMap(source_group=pi53, target_group=pi55))),
        ("suspension_surjective", TodaSuspensionSurjectiveStatement(map=suspension)),
        ("hopf_surjective", TodaHopfInvariantSurjectiveStatement(map=TodaHopfInvariantMap(source_group=pi63, target_group=pi65))),
        ("delta_zero", TodaDeltaZeroStatement(map=TodaDeltaMap(source_group=pi65, target_group=pi42))),
        ("suspension_injective", TodaSuspensionInjectiveStatement(map=suspension)),
        ("isomorphism", TodaSuspensionIsomorphismStatement(map=suspension)),
    )
    return exactness, goal_chain


def select_one_step(catalog_entries, available_steps, goal):
    candidates = [entry for entry in catalog_entries if entry.conclusion_type is type(goal)]
    diagnostics = {"candidate_entries": len(candidates), "matching_rules": 0, "exact_goal_producers": 0}
    producers = []
    for entry in candidates:
        try:
            matches = find_inference_matches_for_rule(entry.rule, available_steps)
        except (TypeError, ValueError, RuntimeError) as error:
            diagnostics.setdefault("errors", []).append({"key": entry.key, "error": str(error)})
            continue
        if matches:
            diagnostics["matching_rules"] += 1
        for match in matches:
            try:
                new_step = apply_inference_match(match)
            except (TypeError, ValueError, RuntimeError) as error:
                diagnostics.setdefault("errors", []).append({"key": entry.key, "error": str(error)})
                continue
            if new_step.conclusion == goal:
                producers.append((entry, new_step))
    diagnostics["exact_goal_producers"] = len(producers)
    if not producers:
        return None, diagnostics
    # No name-based selection: choose the first candidate that actually proves the exact target.
    entry, step = producers[0]
    diagnostics["selected_catalog_key"] = entry.key
    diagnostics["selected_rule_name_for_reporting_only"] = entry.rule.name
    diagnostics["selected_premise_types"] = [type(p.conclusion).__name__ for p in step.premises]
    diagnostics["selected_premises_are_existing_or_new_real_steps"] = all(
        any(p is present for present in available_steps) for p in step.premises
    )
    return step, diagnostics


def main():
    repository = build_standard_production_proof_repository()
    scope = build_repository_proof_scope(repository)
    catalog = build_standard_production_applicability_catalog()
    all_steps = unique_by_identity(node.proof_step for node in scope.nodes)
    exactness, goals = build_goals()
    exactness_candidates = [tuple(step for step in all_steps if step.conclusion == expected and step.rule is ProofRule.GIVEN) for expected in exactness]
    prop_candidates = unique_by_identity(
        step for step in all_steps
        if isinstance(step.conclusion, TodaProp51FiniteDimensionalStatement)
        and step.rule is ProofRule.INFERENCE
    )
    relation_candidates = unique_by_identity(
        step for step in all_steps
        if isinstance(step.conclusion, Relation)
        and step.rule is ProofRule.INFERENCE
        and step.inference_rule is not None
        and step.inference_rule.name == "equality transitivity"
    )
    output = {
        "scope": "Name-free RULE selection by typed exact intermediate goals + real premise matches; mathematical subgoal chain is specified; existing relation provenance filter is still name-based",
        "production_scope_nodes": len(scope.nodes),
        "catalog_entries": len(catalog.entries()),
        "exactness_candidate_counts": [len(x) for x in exactness_candidates],
        "proposition_candidate_count": len(prop_candidates),
        "hopf_relation_candidate_count": len(relation_candidates),
        "pairs_attempted": 0,
        "success": False,
    }
    if not all(exactness_candidates):
        output["status"] = "MISSING_EXACTNESS"
        return output
    baseline = tuple(items[0] for items in exactness_candidates)
    for prop in prop_candidates:
        for relation in relation_candidates:
            output["pairs_attempted"] += 1
            current = list((prop, relation) + baseline)
            diagnostics = []
            successful = True
            for label, goal in goals:
                new_step, detail = select_one_step(catalog.entries(), tuple(current), goal)
                diagnostics.append({"stage": label, **detail})
                if new_step is None:
                    successful = False
                    break
                current.append(new_step)
            if successful:
                output["success"] = True
                output["status"] = "SEMANTIC_RULE_SELECTION_REAL_PROOF_SUCCESS"
                output["stages"] = diagnostics
                output["new_inference_steps"] = len(goals)
                output["selected_initial_provenance"] = [
                    {"type": type(step.conclusion).__name__, "rule": step.rule.name,
                     "inference_rule": step.inference_rule.name if step.inference_rule else None}
                    for step in (prop, relation) + baseline
                ]
                output["all_generated_steps_are_inferences"] = all(
                    step.rule is ProofRule.INFERENCE and step.inference_rule is not None
                    for step in current[6:]
                )
                return output
            if output["pairs_attempted"] == 1:
                output["first_pair_diagnostics"] = diagnostics
    output["status"] = "NO_COMPATIBLE_CHAIN_FOUND"
    return output


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    target = Path("phase161_semantic_selection_execution.json")
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote:", target.resolve())
    if not result["success"]:
        raise SystemExit(1)
