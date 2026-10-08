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
    entry = matching[0]
    patterns = entry.rule.premise_patterns
    generated = (injective, surjective)
    pattern_checks = []
    for index, pattern in enumerate(patterns):
        statement = generated[index] if index < len(generated) else None
        if statement is None:
            pattern_checks.append({
                "index": index,
                "statement_available": False,
                "semantic_match": False,
                "given_step_match": False,
                "required_proof_rule": None,
                "required_provenance_simulation_match": False,
            })
            continue
        given_step = ProofStep(
            conclusion=statement, premises=(), rule=ProofRule.GIVEN
        )
        required_rule = pattern.proof_rule or ProofRule.GIVEN
        simulated_step = ProofStep(
            conclusion=statement, premises=(), rule=required_rule
        )
        semantic_match = (
            (pattern.statement_type is None or isinstance(statement, pattern.statement_type))
            and (pattern.statement_pattern is None or
                 match_statement_pattern(pattern.statement_pattern, statement) is not None)
            and (pattern.relation_type is None or
                 getattr(statement, "relation_type", None) == pattern.relation_type)
        )
        pattern_checks.append({
            "index": index,
            "statement_available": True,
            "statement_type": type(statement).__name__,
            "required_statement_type": (
                pattern.statement_type.__name__ if pattern.statement_type is not None else None
            ),
            "required_proof_rule": (
                pattern.proof_rule.name if pattern.proof_rule is not None else None
            ),
            "semantic_match": semantic_match,
            "given_step_match": match_premise_pattern(pattern, given_step) is not None,
            "required_provenance_simulation_match": (
                match_premise_pattern(pattern, simulated_step) is not None
            ),
            "has_statement_pattern": pattern.statement_pattern is not None,
            "simulated_step_is_actual_proof": False,
        })

    result = {
        "scope": "Single production final rule; separate statement matching and proof provenance; no proof execution",
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
        "generated_both_premises_semantically": (
            len(patterns) == 2 and all(item["semantic_match"] for item in pattern_checks)
        ),
        "both_premises_simulated_provenance_compatible": (
            len(patterns) == 2
            and all(item["required_provenance_simulation_match"] for item in pattern_checks)
        ),
        "proof_generated": False,
        "limitations": [
            "A synthetic INFERENCE step is only for checking the pattern contract; it is NOT a derivation.",
            "Actual INFERENCE proof steps must be independently derived before running the final rule.",
            "Only one final-rule family is selected by name for this audit.",
            "Production catalog and inference rules are unchanged.",
        ],
    }
    output_path = Path.cwd() / "phase161_final_goal_pattern_provenance_fix.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Wrote: {output_path}")
    if not result["generated_both_premises_semantically"]:
        raise SystemExit("Semantic premise matching failed")
    if not result["both_premises_simulated_provenance_compatible"]:
        raise SystemExit("Premise pattern incompatibility beyond GIVEN/INFERENCE provenance")


if __name__ == "__main__":
    run_audit()
