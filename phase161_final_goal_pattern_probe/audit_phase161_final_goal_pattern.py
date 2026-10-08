import json
from pathlib import Path

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from proof import (
    PatternVariable,
    ProofRule,
    ProofStep,
    match_premise_pattern,
    match_statement_pattern,
    substitute_statement_pattern,
)
from standard_production_applicability_catalog import (
    build_standard_production_applicability_catalog,
)
from toda_rules import (
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def run_audit():
    source = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    target = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    goal_map = TodaSuspensionMap(source_group=source, target_group=target)
    goal = TodaSuspensionIsomorphismStatement(map=goal_map)

    variable = PatternVariable(name="goal_suspension_map")
    goal_pattern = TodaSuspensionIsomorphismStatement(map=variable)
    bindings = match_statement_pattern(goal_pattern, goal)
    if bindings is None:
        raise AssertionError("goal pattern did not match")
    recovered_goal = substitute_statement_pattern(goal_pattern, bindings)
    injective = substitute_statement_pattern(
        TodaSuspensionInjectiveStatement(map=variable), bindings
    )
    surjective = substitute_statement_pattern(
        TodaSuspensionSurjectiveStatement(map=variable), bindings
    )

    catalog = build_standard_production_applicability_catalog()
    matching = [
        entry for entry in catalog.entries()
        if entry.rule.name == "Toda Proposition 5.3 n=3 suspension isomorphism"
        and entry.conclusion_type is TodaSuspensionIsomorphismStatement
    ]
    if not matching:
        raise AssertionError("production final rule not found")

    # Choose a single production entry for a narrow, read-only compatibility check.
    entry = matching[0]
    patterns = entry.rule.premise_patterns
    generated = (injective, surjective)
    pattern_checks = []
    for index, pattern in enumerate(patterns):
        # These are synthetic GIVEN steps used ONLY for matching, not proof evidence.
        synthetic_step = ProofStep(
            conclusion=generated[index], premises=(), rule=ProofRule.GIVEN
        ) if index < len(generated) else None
        pattern_checks.append({
            "index": index,
            "statement_type": (
                pattern.statement_type.__name__
                if pattern.statement_type is not None else None
            ),
            "matches_generated_statement": (
                match_premise_pattern(pattern, synthetic_step) is not None
                if synthetic_step is not None else False
            ),
            "has_statement_pattern": pattern.statement_pattern is not None,
        })

    result = {
        "scope": "Single final rule goal-pattern compatibility; no rule mutation, no proof execution",
        "goal": repr(goal),
        "goal_binding_count": len(bindings),
        "round_trip_goal_equal": recovered_goal == goal,
        "injective_generated": repr(injective),
        "surjective_generated": repr(surjective),
        "same_map_in_both_premises": injective.map == surjective.map == goal.map,
        "production_rule_matching_name_count": len(matching),
        "selected_production_catalog_key": entry.key,
        "original_rule_fixed_point_safe": entry.fixed_point_safe,
        "rule_premise_count": len(patterns),
        "premise_pattern_checks": pattern_checks,
        "generated_both_premises": (
            len(patterns) == 2
            and all(item["matches_generated_statement"] for item in pattern_checks)
        ),
        "limitations": [
            "Only one final-rule family, selected by name for this focused audit.",
            "No full backward search or independent derivation of premises is performed.",
            "Synthetic GIVEN steps are never registered as mathematical proof facts.",
            "No safety certification or production modification is performed.",
        ],
    }
    output_path = Path.cwd() / "phase161_final_goal_pattern_probe.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Wrote: {output_path}")
    if not result["generated_both_premises"]:
        raise SystemExit("Premise pattern compatibility failed; see diagnostic JSON")


if __name__ == "__main__":
    run_audit()
