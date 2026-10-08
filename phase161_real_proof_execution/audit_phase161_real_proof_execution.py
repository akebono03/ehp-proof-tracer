from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionInjectiveStatement,
    TodaSuspensionMap,
    TodaSuspensionSurjectiveStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from proof import ProofRule, Relation, run_inference_until_stable_with_history
from repository_proof_scope import build_repository_proof_scope
from standard_production_repository import build_standard_production_proof_repository
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from toda_rules import TodaProp42ExactnessStatement, TodaProp51FiniteDimensionalStatement


RULE_NAMES = (
    "Toda Proposition 5.1 n=3 Delta injectivity",
    "Toda Proposition 5.3 n=3 Delta injectivity implies Hopf zero",
    "Toda Proposition 5.3 n=3 Hopf zero implies suspension surjective",
    "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity",
    "Toda Proposition 5.3 n=3 Hopf surjective implies Delta zero",
    "Toda Proposition 5.3 n=3 Delta zero implies suspension injective",
    "Toda Proposition 5.3 n=3 suspension isomorphism",
)


def unique_by_identity(steps):
    seen = set()
    result = []
    for step in steps:
        if id(step) not in seen:
            seen.add(id(step))
            result.append(step)
    return tuple(result)


def make_expected_exactness():
    g = lambda d, n: TodaPrimaryGroup(group_dimension=d, sphere_dimension=n)
    windows = (
        (g(5, 3), g(5, 5), g(3, 2), EHP_H_MAP, EHP_DELTA_MAP),
        (g(4, 2), g(5, 3), g(5, 5), EHP_E_MAP, EHP_H_MAP),
        (g(6, 3), g(6, 5), g(4, 2), EHP_H_MAP, EHP_DELTA_MAP),
        (g(6, 5), g(4, 2), g(5, 3), EHP_DELTA_MAP, EHP_E_MAP),
    )
    return tuple(
        TodaProp42ExactnessStatement(
            window=TodaEHPExactnessWindow(
                source_term=a, middle_term=b, target_term=c,
                first_map=first, second_map=second,
            )
        )
        for a, b, c, first, second in windows
    )


def main():
    repo = build_standard_production_proof_repository()
    catalog = build_standard_production_applicability_catalog()
    scope = build_repository_proof_scope(repo)
    all_steps = unique_by_identity(node.proof_step for node in scope)
    entries = catalog.entries()
    exact_goals = make_expected_exactness()
    exactness_matches = [
        tuple(step for step in all_steps if step.conclusion == expected)
        for expected in exact_goals
    ]
    prop_candidates = unique_by_identity(
        step for step in all_steps
        if isinstance(step.conclusion, TodaProp51FiniteDimensionalStatement)
        and step.rule == ProofRule.INFERENCE
    )
    hopf_candidates = unique_by_identity(
        step for step in all_steps
        if isinstance(step.conclusion, Relation)
        and step.rule == ProofRule.INFERENCE
        and step.inference_rule is not None
        and step.inference_rule.name == "equality transitivity"
    )
    selected_rules = []
    rule_details = []
    for name in RULE_NAMES:
        choices = [entry for entry in entries if entry.rule.name == name]
        rule_details.append({"name": name, "catalog_entries": len(choices)})
        if choices:
            selected_rules.append(choices[0].rule)
    goal_map = TodaSuspensionMap(
        source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
        target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
    )
    expected = (
        TodaSuspensionInjectiveStatement(map=goal_map),
        TodaSuspensionSurjectiveStatement(map=goal_map),
        TodaSuspensionIsomorphismStatement(map=goal_map),
    )
    result = {
        "scope": "Real existing Production ProofSteps as premises; focused seven already-identified rules; no target ancestry selection and no synthetic premise",
        "production_scope_nodes": len(scope),
        "unique_production_steps": len(all_steps),
        "catalog_entries": len(entries),
        "exactness_matches": [len(x) for x in exactness_matches],
        "proposition_candidates": len(prop_candidates),
        "hopf_relation_candidates": len(hopf_candidates),
        "rule_selection": rule_details,
        "pairs_attempted": 0,
        "success": False,
    }
    if not all(exactness_matches) or len(selected_rules) != 7:
        result["status"] = "MISSING_REAL_PREMISE_OR_RULE"
        return result
    baseline = tuple(matches[0] for matches in exactness_matches)
    if any(step.rule != ProofRule.GIVEN for step in baseline):
        result["status"] = "EXACTNESS_PROVENANCE_DIFFERS"
        return result
    for prop in prop_candidates:
        for hopf in hopf_candidates:
            result["pairs_attempted"] += 1
            real_initial_steps = (prop, hopf) + baseline
            try:
                proof_result = run_inference_until_stable_with_history(
                    tuple(selected_rules), real_initial_steps
                )
            except (TypeError, ValueError, RuntimeError) as error:
                result.setdefault("execution_errors", []).append(
                    {"type": type(error).__name__, "message": str(error)}
                )
                continue
            derived = {}
            for label, target in zip(("injective", "surjective", "isomorphism"), expected):
                matches = [step for step in proof_result.steps if step.conclusion == target]
                derived[label] = {
                    "found": bool(matches),
                    "is_new_inference": any(
                        step.rule == ProofRule.INFERENCE
                        and step not in real_initial_steps
                        and step.inference_rule is not None
                        for step in matches
                    ),
                    "count": len(matches),
                }
            if all(derived[x]["is_new_inference"] for x in derived):
                result["success"] = True
                result["status"] = "REAL_PRODUCTION_PREMISES_DERIVED_ALL_THREE"
                result["derived"] = derived
                result["selected_provenance"] = [
                    {"statement_type": type(step.conclusion).__name__,
                     "proof_rule": step.rule.name,
                     "inference_rule": step.inference_rule.name if step.inference_rule else None}
                    for step in real_initial_steps
                ]
                result["new_step_count"] = len(proof_result.steps) - len(real_initial_steps)
                return result
    result["status"] = "NO_SUCCESS_WITH_SELECTED_PRODUCTION_CANDIDATES"
    return result


if __name__ == "__main__":
    outcome = main()
    print(json.dumps(outcome, indent=2, ensure_ascii=False))
    target = Path("phase161_real_proof_execution.json")
    target.write_text(json.dumps(outcome, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote:", target.resolve())
    if not outcome["success"]:
        raise SystemExit(1)
