"""Phase 161 read-only: Phase 59 expected identities vs actual production assets.

Phase 59 helper is used ONLY as an oracle for expected statements/rule names.
It does not supply repository entries or catalog entries to production search.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))

from repository_inference import repository_available_steps
from repository_proof_scope import build_repository_proof_scope
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from standard_production_repository import build_standard_production_proof_repository
from test_phase59_n3_ehp_chain import build_phase59_3_data


def rule_factory(rule):
    builder = rule.conclusion_builder
    qualname = getattr(builder, '__qualname__', '') if callable(builder) else ''
    return qualname.split('.<locals>.')[0].split('.')[-1] if '.<locals>.' in qualname else qualname


def step_locations(step, direct_steps, scope):
    return {
        'direct_repository': any(s.conclusion == step.conclusion for s in direct_steps),
        'scope_matches': [
            {'root_key': n.root_entry.key, 'depth': n.shortest_depth,
             'rule_kind': n.proof_step.rule.name,
             'inference_rule': getattr(n.proof_step.inference_rule, 'name', None)}
            for n in scope.nodes if n.proof_step.conclusion == step.conclusion
        ],
    }


def main():
    production_repository = build_standard_production_proof_repository()
    catalog = build_standard_production_applicability_catalog()
    direct_steps = repository_available_steps(production_repository)
    scope = build_repository_proof_scope(production_repository)
    # Reference oracle only; NOT a production seed or catalog replacement.
    baseline = build_phase59_3_data()
    premise_names = ('prop51_step', 'hopf_eta5_step', 'h_delta_5_step',
                     'e_h_5_step', 'h_delta_6_step', 'delta_e_6_step')
    premises = []
    for key in premise_names:
        step = baseline[key]
        locations = step_locations(step, direct_steps, scope)
        premises.append({
            'key': key,
            'statement_type': type(step.conclusion).__name__,
            'phase59_rule_kind': step.rule.name,
            'phase59_inference_rule': getattr(step.inference_rule, 'name', None),
            **locations,
            'usable_as_current_search_initial_premise': locations['direct_repository'],
        })
    rule_rows = []
    for i, rule in enumerate(baseline['rules']):
        factory = rule_factory(rule)
        candidates = [e for e in catalog.entries() if rule_factory(e.rule) == factory]
        rule_rows.append({
            'phase59_rule_index': i,
            'factory': factory,
            'name': rule.name,
            'premise_count': len(rule.premise_patterns),
            'production_catalog_entries': len(candidates),
            'catalog_matches': [
                {'key': e.key, 'name': e.rule.name,
                 'fixed_point_safe': e.fixed_point_safe,
                 'relevance_category': e.relevance_category.value,
                 'same_object_as_oracle_rule': e.rule is rule}
                for e in candidates
            ],
            'any_search_eligible': any(e.fixed_point_safe for e in candidates),
            'safety_conclusion': 'NOT_CERTIFIED_BY_THIS_AUDIT',
        })
    result = {
        'scope': 'Actual production repository/catalog; Phase59 is oracle ONLY',
        'production_repository_root_count': len(production_repository.entries()),
        'production_repository_keys': [e.key for e in production_repository.entries()],
        'production_scope_node_count': len(scope.nodes),
        'production_catalog_count': len(catalog.entries()),
        'production_catalog_safe_count': sum(e.fixed_point_safe for e in catalog.entries()),
        'seven_rules': rule_rows,
        'six_premises': premises,
        'audit_limitations': [
            'Catalog presence does not establish mathematical soundness or fixed-point safety.',
            'Ancestry occurrence does not mean repository_available_steps exposes the premise.',
            'No search policy or production repository was modified.',
            'No full pytest suite was executed.',
        ],
    }
    target = ROOT / 'phase161_production_seven_six_audit.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print('Wrote:', target)


if __name__ == '__main__':
    main()
