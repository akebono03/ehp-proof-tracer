"""Read-only Phase 161 proof-search audit for pi_5^3.
Run in an existing ehp-proof-tracer checkout. Does not modify source files.
"""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))

from test_phase59_n3_ehp_chain import build_phase59_3_data
from proof_repository import ProofRepository, ProofRepositoryEntry
from rule_catalog import InferenceRuleCatalog, InferenceRuleCatalogEntry, find_goal_compatible_rule_entries
from repository_inference import (
    repository_available_steps,
    build_depth_two_producer_search_report,
    derive_goal_from_repository_with_depth_two_producers,
)
from proof import ProofRule


def summarize_step(step):
    if step is None:
        return None
    return {
        'statement_type': type(step.conclusion).__name__,
        'rule_type': step.rule.name,
        'inference_rule': getattr(getattr(step, 'inference_rule', None), 'name', None),
        'premise_types': [type(p.conclusion).__name__ for p in step.premises],
    }


def main():
    d = build_phase59_3_data()
    goal = d['expected_suspension_isomorphism']
    premises = d['premise_steps']
    rules = d['rules']
    repository = ProofRepository()
    for i, step in enumerate(premises):
        repository.register(ProofRepositoryEntry(
            key=f'phase161.audit.premise.{i}', step=step,
            phase='161', theorem='read-only pi5_3 search audit'))
    catalog = InferenceRuleCatalog()
    # This catalog is constructed explicitly from Phase 59's already selected rules.
    # It does NOT establish that the production catalog can discover them.
    for i, rule in enumerate(rules):
        conclusion_type = type(next(
            step.conclusion for step in d['result'].steps
            if getattr(step, 'inference_rule', None) is rule
        ))
        catalog.register(InferenceRuleCatalogEntry(
            key=f'phase161.audit.rule.{i}', rule=rule,
            conclusion_type=conclusion_type, fixed_point_safe=True,
        ))
    compatible = find_goal_compatible_rule_entries(catalog, goal)
    report = build_depth_two_producer_search_report(repository, catalog, goal)
    result = derive_goal_from_repository_with_depth_two_producers(repository, catalog, goal)
    data = {
        'scope': 'Phase 59 explicitly seeded premises and rules (not goal-only production search)',
        'goal_type': type(goal).__name__,
        'premise_count': len(premises),
        'given_count': sum(s.rule == ProofRule.GIVEN for s in premises),
        'catalog_rule_count': len(rules),
        'compatible_final_rules': [e.key for e in compatible],
        'search_report_status': report.status.name,
        'producer_node_count': len(report.search_result.producer_nodes) if report.search_result else 0,
        'goal_derived': result.goal_step is not None,
        'goal_step': summarize_step(result.goal_step),
        'phase59_goal_present': any(s.conclusion == goal for s in d['result'].steps),
        'note': 'Failure is diagnostic only; depth-2 bounded search is not the Phase 59 full forward chain.',
    }
    output = ROOT / 'phase161_proof_search_audit.json'
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f'Wrote: {output}')


if __name__ == '__main__':
    main()
