"""Read-only diagnostic of Phase 59 intermediate goals, with a seeded audit catalog."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))

from proof import ProofRule
from proof_repository import ProofRepository, ProofRepositoryEntry
from repository_inference import build_depth_two_producer_search_report
from rule_catalog import InferenceRuleCatalog, InferenceRuleCatalogEntry, find_goal_compatible_rule_entries
from test_phase59_n3_ehp_chain import build_phase59_3_data


def main():
    data = build_phase59_3_data()
    repository = ProofRepository()
    for index, step in enumerate(data['premise_steps']):
        repository.register(ProofRepositoryEntry(
            key=f'phase161.boundary.premise.{index}',
            step=step,
            phase='161',
            theorem='read-only boundary audit',
        ))
    catalog = InferenceRuleCatalog()
    derived_steps = data['result'].steps
    for index, rule in enumerate(data['rules']):
        matching_steps = [step for step in derived_steps if getattr(step, 'inference_rule', None) is rule]
        if not matching_steps:
            raise RuntimeError(f'Rule has no produced step: {rule.name}')
        catalog.register(InferenceRuleCatalogEntry(
            key=f'phase161.boundary.rule.{index}',
            rule=rule,
            conclusion_type=type(matching_steps[0].conclusion),
            fixed_point_safe=True,
        ))

    goals = [
        ('delta_injective', data['expected_delta_injective']),
        ('hopf_zero', data['expected_hopf_zero']),
        ('suspension_surjective', data['expected_suspension_surjective']),
        ('hopf_surjective', data['expected_hopf_surjective']),
        ('delta_zero', data['expected_delta_zero']),
        ('suspension_injective', data['expected_suspension_injective']),
        ('suspension_isomorphism', data['expected_suspension_isomorphism']),
    ]
    report_rows = []
    for name, goal in goals:
        matching = find_goal_compatible_rule_entries(catalog, goal)
        report = build_depth_two_producer_search_report(repository, catalog, goal)
        proved = next((s for s in derived_steps if s.conclusion == goal), None)
        ancestor_ids = set()
        def depth(step, visiting):
            if id(step) in visiting:
                raise ValueError('cycle in Phase 59 proof graph')
            if not step.premises:
                return 0
            return 1 + max(depth(p, visiting | {id(step)}) for p in step.premises)
        report_rows.append({
            'goal': name,
            'goal_type': type(goal).__name__,
            'catalog_matching_rules': [e.key for e in matching],
            'search_status': report.status.name,
            'search_producer_nodes': len(report.search_result.producer_nodes) if report.search_result else 0,
            'forward_derived': proved is not None,
            'forward_proof_depth': depth(proved, set()) if proved is not None else None,
            'forward_rule': getattr(getattr(proved, 'inference_rule', None), 'name', None),
        })
    result = {
        'scope': 'Read-only seeded Phase 59 rule/premise catalog, NOT production goal-only search',
        'initial_premises': len(data['premise_steps']),
        'registered_rules': len(data['rules']),
        'goals': report_rows,
    }
    output = ROOT / 'phase161_search_boundary_audit.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'Wrote: {output}')


if __name__ == '__main__':
    main()
