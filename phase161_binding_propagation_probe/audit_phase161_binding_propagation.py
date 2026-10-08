import json
from dataclasses import is_dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
from toda_rules import TodaSuspensionInjectiveStatement, TodaSuspensionSurjectiveStatement
from proof import PatternVariable, match_statement_pattern, substitute_statement_pattern, merge_variable_bindings, PremisePattern, ProofStep, ProofRule, match_premise_pattern
from standard_production_applicability_catalog import build_standard_production_applicability_catalog


def main():
    source = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    target = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    suspension = TodaSuspensionMap(source_group=source, target_group=target)
    goal = TodaSuspensionIsomorphismStatement(map=suspension)
    variable = PatternVariable(name="phase161_suspension_map")
    goal_template = TodaSuspensionIsomorphismStatement(map=variable)
    bindings = match_statement_pattern(goal_template, goal)
    assert bindings is not None and len(bindings) == 1
    injective_template = TodaSuspensionInjectiveStatement(map=variable)
    surjective_template = TodaSuspensionSurjectiveStatement(map=variable)
    injective = substitute_statement_pattern(injective_template, bindings)
    surjective = substitute_statement_pattern(surjective_template, bindings)
    assert injective.map == goal.map and surjective.map == goal.map

    other = TodaSuspensionMap(
        source_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        target_group=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4),
    )
    incompatible = match_statement_pattern(goal_template, TodaSuspensionIsomorphismStatement(map=other))
    inconsistent = merge_variable_bindings(bindings + incompatible)
    assert inconsistent is None
    positive = PremisePattern(statement_type=type(injective), statement_pattern=injective_template)
    positive_match = match_premise_pattern(positive, ProofStep(conclusion=injective, premises=(), rule=ProofRule.GIVEN))
    negative_match = match_premise_pattern(positive, ProofStep(conclusion=TodaSuspensionInjectiveStatement(map=other), premises=(), rule=ProofRule.GIVEN))
    assert positive_match is not None
    assert merge_variable_bindings(bindings + positive_match) is not None
    assert merge_variable_bindings(bindings + negative_match) is None

    catalog = build_standard_production_applicability_catalog()
    candidates = [e for e in catalog.entries() if e.conclusion_type is type(goal)]
    output = []
    for e in candidates:
        rule = e.rule
        pattern = rule.conclusion_pattern
        match_status = "NO_CONCLUSION_PATTERN"
        matched_count = None
        if pattern is not None:
            if is_dataclass(pattern):
                try:
                    result = match_statement_pattern(pattern, goal)
                    match_status = "MATCH" if result is not None else "NO_MATCH"
                    matched_count = len(result) if result is not None else None
                except (TypeError, ValueError) as error:
                    match_status = f"MATCH_ERROR:{type(error).__name__}"
            else:
                match_status = "NON_DATACLASS_PATTERN"
        output.append({
            "catalog_key": e.key,
            "rule_name": rule.name,
            "premise_count": len(rule.premise_patterns),
            "has_conclusion_builder": callable(rule.conclusion_builder),
            "pattern_status": match_status,
            "match_binding_count": matched_count,
            "premise_statement_types": [p.statement_type.__name__ if p.statement_type else None for p in rule.premise_patterns],
        })
    report = {
        "scope": "Read-only existing matcher / substitution probe, production catalog, no family-name selection",
        "goal_type": type(goal).__name__,
        "map_whole_variable_binding": len(bindings),
        "injective_substitution_matches_goal_map": injective.map == goal.map,
        "surjective_substitution_matches_goal_map": surjective.map == goal.map,
        "different_map_binding_conflict_rejected": inconsistent is None,
        "positive_premise_binding_compatible": merge_variable_bindings(bindings + positive_match) is not None,
        "negative_premise_binding_rejected": merge_variable_bindings(bindings + negative_match) is None,
        "production_goal_type_entries": len(candidates),
        "production_conclusion_pattern_match_entries": sum(x["pattern_status"] == "MATCH" for x in output),
        "production_no_conclusion_pattern_entries": sum(x["pattern_status"] == "NO_CONCLUSION_PATTERN" for x in output),
        "candidate_diagnostics": output,
        "limitations": [
            "Template demonstrates whole-map-variable bindings; it is not a production rule's own conclusion pattern.",
            "A missing conclusion pattern does not imply a rule is inapplicable; conclusion builders may compute a goal after premises bind.",
            "Does not enumerate or execute all compatible candidate chains; no safety certification or full autonomous goal-only proof.",
        ],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    Path("phase161_binding_propagation_probe.json").write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
