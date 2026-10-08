"""Focused read-only candidate conclusion-builder compatibility experiment."""
import json
from pathlib import Path

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaHopfInvariantMap,
    TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from proof import (
    PatternVariable, ProofRule, ProofStep, apply_inference_match,
    find_inference_matches_for_rule, match_premise_pattern,
    match_statement_pattern, substitute_statement_pattern,
)
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from toda_rules import (
    TodaDeltaZeroStatement, TodaHopfInvariantZeroStatement,
    TodaProp42ExactnessStatement, TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def examine_branch(catalog, branch_name, goal, zero, exactness):
    results = []
    examined = 0
    for entry in catalog.entries():
        if entry.conclusion_type is not type(goal):
            continue
        patterns = entry.rule.premise_patterns
        if len(patterns) != 2:
            continue
        steps_by_position = []
        for statement in (zero, exactness):
            options = []
            for index, pattern in enumerate(patterns):
                assumed_rule = pattern.proof_rule or ProofRule.GIVEN
                hypothetical = ProofStep(conclusion=statement, premises=(), rule=assumed_rule)
                if match_premise_pattern(pattern, hypothetical) is not None:
                    options.append((index, hypothetical))
            steps_by_position.append(options)
        if not any(a != b for a, _ in steps_by_position[0] for b, _ in steps_by_position[1]):
            continue
        examined += 1
        record = {"catalog_key": entry.key, "rule_name": entry.rule.name,
                  "production_safe": entry.fixed_point_safe,
                  "premise_signature_matches": True,
                  "matches_found": 0, "goal_equal": False,
                  "generated_conclusions": [], "errors": []}
        arrangements = []
        for i, z in steps_by_position[0]:
            for j, e in steps_by_position[1]:
                if i != j:
                    order = [None, None]
                    order[i] = z
                    order[j] = e
                    arrangements.append(tuple(order))
        for order in arrangements:
            try:
                matches = find_inference_matches_for_rule(entry.rule, order)
                record["matches_found"] += len(matches)
                for match in matches:
                    try:
                        step = apply_inference_match(match)
                        equal = step.conclusion == goal
                        record["goal_equal"] = record["goal_equal"] or equal
                        repr_value = repr(step.conclusion)
                        if repr_value not in record["generated_conclusions"]:
                            record["generated_conclusions"].append(repr_value)
                    except Exception as exc:
                        record["errors"].append("apply: " + type(exc).__name__ + ": " + str(exc))
            except Exception as exc:
                record["errors"].append("match: " + type(exc).__name__ + ": " + str(exc))
        results.append(record)
    return {"branch": branch_name, "goal": repr(goal), "structural_candidates_examined": examined,
            "guard_compatible_candidates": sum(r["matches_found"] > 0 for r in results),
            "exact_goal_generating_candidates": sum(r["goal_equal"] for r in results),
            "candidates": results}


def main():
    pi42 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi53 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi65 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    pi55 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    suspension = TodaSuspensionMap(source_group=pi42, target_group=pi53)
    goal = TodaSuspensionIsomorphismStatement(map=suspension)
    var = PatternVariable(name="suspension")
    bindings = match_statement_pattern(TodaSuspensionIsomorphismStatement(map=var), goal)
    if bindings is None:
        raise AssertionError("Final goal binding failed")
    injective = substitute_statement_pattern(TodaSuspensionInjectiveStatement(map=var), bindings)
    surjective = substitute_statement_pattern(TodaSuspensionSurjectiveStatement(map=var), bindings)
    delta_zero = TodaDeltaZeroStatement(map=TodaDeltaMap(source_group=pi65, target_group=pi42))
    hopf_zero = TodaHopfInvariantZeroStatement(map=TodaHopfInvariantMap(source_group=pi53, target_group=pi55))
    delta_exact = TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(
        source_term=pi65, middle_term=pi42, target_term=pi53,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP))
    hopf_exact = TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(
        source_term=pi42, middle_term=pi53, target_term=pi55,
        first_map=EHP_E_MAP, second_map=EHP_H_MAP))
    catalog = build_standard_production_applicability_catalog()
    branches = [examine_branch(catalog, "injectivity", injective, delta_zero, delta_exact),
                examine_branch(catalog, "surjectivity", surjective, hopf_zero, hopf_exact)]
    report = {"scope": "Synthetic premise compatibility only; no proof registration; no family name selection or ancestry lookup",
              "catalog_entry_count": len(catalog.entries()), "branches": branches,
              "status": "BOTH_BRANCHES_EXACT_CONCLUSION_COMPATIBLE" if all(b["exact_goal_generating_candidates"] > 0 for b in branches) else "SOME_BRANCH_HAS_NO_EXACT_CONCLUSION_COMPATIBLE_CANDIDATE",
              "limitations": ["Synthetic ProofSteps do NOT establish the premises.",
                              "A matching conclusion is necessary but not sufficient for a valid proof.",
                              "Production safe flags are unchanged; no whole-suite tests."]}
    out = Path.cwd() / "phase161_conclusion_builder_validation.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Wrote:", out)


if __name__ == "__main__":
    main()
