"""Read-only, type/shape-directed second-level EHP subgoal expansion.

Does not select a completed proof, certify rule safety, or register proof steps.
"""
import json
from pathlib import Path

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaHopfInvariantMap,
    TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from proof import PatternVariable, ProofRule, ProofStep, match_premise_pattern, match_statement_pattern, substitute_statement_pattern
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from toda_rules import (
    TodaDeltaZeroStatement, TodaHopfInvariantZeroStatement,
    TodaProp42ExactnessStatement, TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def inspect_candidates(catalog, subgoal, expected_zero, expected_exactness):
    entries = [e for e in catalog.entries() if e.conclusion_type is type(subgoal)]
    relevant = []
    for entry in entries:
        patterns = entry.rule.premise_patterns
        if len(patterns) != 2:
            continue
        checks = []
        for statement in (expected_zero, expected_exactness):
            matched_indices = []
            for index, pattern in enumerate(patterns):
                proof_rule = pattern.proof_rule or ProofRule.GIVEN
                hypothetical = ProofStep(conclusion=statement, premises=(), rule=proof_rule)
                if match_premise_pattern(pattern, hypothetical) is not None:
                    matched_indices.append(index)
            checks.append(matched_indices)
        distinct_matching_slots = any(a != b for a in checks[0] for b in checks[1])
        if distinct_matching_slots:
            relevant.append({
                "key": entry.key,
                "name": entry.rule.name,
                "premise_positions_for_zero": checks[0],
                "premise_positions_for_exactness": checks[1],
                "conclusion_pattern_available": entry.rule.conclusion_pattern is not None,
                "safe_in_production": entry.fixed_point_safe,
                "conclusion_builder_available": entry.rule.conclusion_builder is not None,
            })
    return {"same_conclusion_type_candidates": len(entries), "two_premise_structural_candidates": relevant}


def main():
    pi42 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi53 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi65 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    pi63 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi55 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    suspension = TodaSuspensionMap(source_group=pi42, target_group=pi53)
    goal = TodaSuspensionIsomorphismStatement(map=suspension)
    variable = PatternVariable(name="suspension")
    bindings = match_statement_pattern(TodaSuspensionIsomorphismStatement(map=variable), goal)
    if bindings is None:
        raise AssertionError("Goal pattern did not match")
    injective = substitute_statement_pattern(TodaSuspensionInjectiveStatement(map=variable), bindings)
    surjective = substitute_statement_pattern(TodaSuspensionSurjectiveStatement(map=variable), bindings)
    delta = TodaDeltaMap(source_group=pi65, target_group=pi42)
    hopf = TodaHopfInvariantMap(source_group=pi53, target_group=pi55)
    delta_zero = TodaDeltaZeroStatement(map=delta)
    hopf_zero = TodaHopfInvariantZeroStatement(map=hopf)
    delta_e = TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(
        source_term=pi65, middle_term=pi42, target_term=pi53,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    ))
    e_h = TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(
        source_term=pi42, middle_term=pi53, target_term=pi55,
        first_map=EHP_E_MAP, second_map=EHP_H_MAP,
    ))
    catalog = build_standard_production_applicability_catalog()
    branches = [
        {"branch": "injectivity", "goal": repr(injective),
         "zero_goal": repr(delta_zero), "exactness_goal": repr(delta_e),
         "candidates": inspect_candidates(catalog, injective, delta_zero, delta_e)},
        {"branch": "surjectivity", "goal": repr(surjective),
         "zero_goal": repr(hopf_zero), "exactness_goal": repr(e_h),
         "candidates": inspect_candidates(catalog, surjective, hopf_zero, e_h)},
    ]
    for branch in branches:
        count = len(branch["candidates"]["two_premise_structural_candidates"])
        branch["structural_candidate_found"] = count > 0
        branch["unique_structural_candidate"] = count == 1
    report = {
        "scope": "Two immediate subgoals only; no rule-family-name filter; no target ancestry; no proof execution",
        "goal": repr(goal), "binding_count": len(bindings),
        "same_suspension_map": injective.map == surjective.map == suspension,
        "catalog_entry_count": len(catalog.entries()), "branches": branches,
        "status": "BOTH_SUBGOALS_STRUCTURALLY_EXPANDED" if all(b["structural_candidate_found"] for b in branches) else "INCOMPLETE_STRUCTURAL_EXPANSION",
        "limitations": [
            "Subgoal maps are constructed from EHP dimensions for this focused n=3 trial, not inferred by a general unifier.",
            "A matching premise signature does not prove its conclusion builder produces this exact goal.",
            "Hypothetical proof-rule attributes only test premise pattern contracts; they are not proofs.",
            "No Production mutation, fixed-point safety certification, or pytest execution.",
        ],
    }
    path = Path.cwd() / "phase161_subgoal_backward_probe.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Wrote: {path}")
    if report["status"] != "BOTH_SUBGOALS_STRUCTURALLY_EXPANDED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
