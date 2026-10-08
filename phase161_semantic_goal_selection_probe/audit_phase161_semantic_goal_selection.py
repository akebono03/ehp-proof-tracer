"""Read-only Phase 161 semantic candidate-discovery audit.

No Phase59 imports, no rule-family allowlist, no target proof ancestry selection.
"""
import json
from collections import Counter
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from proof import match_premise_pattern
from repository_proof_scope import build_repository_proof_scope
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from standard_production_repository import build_standard_production_proof_repository


def main():
    repository = build_standard_production_proof_repository()
    catalog = build_standard_production_applicability_catalog()
    scope = build_repository_proof_scope(repository)
    goal = TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )
    entries = catalog.entries()
    # The goal itself drives this set.  No names, families or proof ancestry.
    levels = []
    wanted_types = {type(goal)}
    selected_types = set()
    for depth in range(4):
        new_types = wanted_types - selected_types
        if not new_types:
            break
        selected_types.update(new_types)
        level_entries = [entry for entry in entries if entry.conclusion_type in new_types]
        premise_types = set()
        for entry in level_entries:
            for pattern in entry.rule.premise_patterns:
                if pattern.statement_type is not None:
                    premise_types.add(pattern.statement_type)
        levels.append({
            'depth': depth,
            'conclusion_types': sorted(t.__name__ for t in new_types),
            'candidate_entry_count': len(level_entries),
            'distinct_rule_identities': len({id(entry.rule) for entry in level_entries}),
            'premise_types': sorted(t.__name__ for t in premise_types),
            'candidate_samples': [
                {'key': entry.key, 'name': entry.rule.name, 'safe': entry.fixed_point_safe,
                 'premise_count': len(entry.rule.premise_patterns)}
                for entry in level_entries[:12]
            ],
        })
        wanted_types.update(premise_types)

    final_entries = [entry for entry in entries if entry.conclusion_type is type(goal)]
    # Detect *structural* candidates.  This is not proof of goal-specific applicability.
    goal_matching_pattern_entries = [
        entry for entry in final_entries
        if entry.rule.conclusion_pattern == goal
    ]
    scope_steps = {}
    for node in scope.nodes:
        scope_steps[id(node.proof_step)] = node.proof_step
    steps = tuple(scope_steps.values())
    type_occurrence = Counter(type(step.conclusion).__name__ for step in steps)

    # Which goal-candidate premise patterns already match an established fact?
    premise_availability = []
    for entry in final_entries:
        patterns = entry.rule.premise_patterns
        matches = []
        for pattern in patterns:
            matched = 0
            for step in steps:
                if match_premise_pattern(pattern, step) is not None:
                    matched += 1
            matches.append(matched)
        premise_availability.append({
            'key': entry.key,
            'rule': entry.rule.name,
            'premise_match_counts_in_production_scope': matches,
            'all_premises_have_individual_matches': all(n > 0 for n in matches),
            'conclusion_pattern_equals_goal': entry.rule.conclusion_pattern == goal,
        })

    report = {
        'scope': 'Production catalog and scope, goal-derived statement-type closure; no rule name list and no goal proof ancestry selection',
        'goal': repr(goal),
        'repository_roots': len(repository.entries()),
        'production_scope_nodes': len(scope.nodes),
        'unique_scope_steps': len(steps),
        'catalog_entries': len(entries),
        'fixed_point_safe_entries': sum(entry.fixed_point_safe for entry in entries),
        'final_goal_type_candidates': len(final_entries),
        'final_exact_conclusion_pattern_candidates': len(goal_matching_pattern_entries),
        'semantic_type_levels': levels,
        'final_premise_pattern_availability': premise_availability,
        'scope_statement_type_counts': {k: type_occurrence[k] for k in sorted(type_occurrence) if k in {t.__name__ for t in wanted_types}},
        'status': 'CANDIDATE_DISCOVERY_ONLY',
        'not_yet_proven': [
            'Rule soundness and fixed-point safety',
            'Unique goal-specific final rule by meaning instead of type alone',
            'Binding-compatible simultaneous premise selection',
            'Automatic proof construction without prespecified rule families',
        ],
    }
    output_path = Path.cwd() / 'phase161_semantic_goal_selection_probe.json'
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    # Compact console summary; full candidate data lives in JSON.
    summary = {k: report[k] for k in (
        'scope', 'repository_roots', 'production_scope_nodes', 'unique_scope_steps',
        'catalog_entries', 'fixed_point_safe_entries', 'final_goal_type_candidates',
        'final_exact_conclusion_pattern_candidates', 'semantic_type_levels', 'status', 'not_yet_proven'
    )}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f'Wrote: {output_path}')


if __name__ == '__main__':
    main()
