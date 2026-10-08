import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from repository_inference import repository_available_steps, build_depth_two_producer_search_report, execute_depth_two_producer_search
from rule_catalog import find_goal_compatible_rule_entries
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from standard_production_repository import build_standard_production_proof_repository


def run():
    repository = build_standard_production_proof_repository()
    catalog = build_standard_production_applicability_catalog()
    goal = TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )
    steps = repository_available_steps(repository)
    matching_types = [e for e in catalog.entries() if e.conclusion_type is type(goal)]
    compatible = find_goal_compatible_rule_entries(catalog, goal)
    result = {
        'scope': 'Actual standard production repository and applicability catalog; no Phase 59 test seeds',
        'repository_entry_count': len(repository.entries()),
        'repository_entry_keys': [e.key for e in repository.entries()],
        'available_step_count': len(steps),
        'catalog_entry_count': len(catalog.entries()),
        'safe_catalog_entry_count': sum(1 for e in catalog.entries() if e.fixed_point_safe),
        'goal_type_catalog_count': len(matching_types),
        'goal_type_entries': [{'key': e.key, 'rule': e.rule.name, 'safe': e.fixed_point_safe} for e in matching_types],
        'goal_compatible_entry_count': len(compatible),
        'goal_initially_available': any(s.conclusion == goal for s in steps),
        'depth_results': [],
    }
    for depth in (2, 3, 4):
        report = build_depth_two_producer_search_report(repository, catalog, goal, max_depth=depth)
        item = {
            'max_depth': depth,
            'report_status': report.status.name,
            'producer_nodes': len(report.search_result.producer_nodes) if report.search_result else 0,
        }
        if report.status.name in ('SUCCESS', 'GOAL_ALREADY_AVAILABLE'):
            execution = execute_depth_two_producer_search(repository, catalog, goal, max_depth=depth)
            item['execution_status'] = execution.report.status.name
            item['goal_derived'] = bool(execution.repository_inference_result and execution.repository_inference_result.goal_step)
        result['depth_results'].append(item)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)
    Path('phase161_production_integration_audit.json').write_text(output + '\n', encoding='utf-8')


if __name__ == '__main__':
    run()
