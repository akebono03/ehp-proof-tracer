"""R4-R11 read-only comparison of typed reference and provider candidate paths."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = Path(__file__).resolve().parent / 'audit_output'


def brief(expansions):
    return [{'rule': getattr(x.rule, 'name', type(x.rule).__name__),
             'subgoals': [repr(g) for g in x.subgoals]}
            for x in expansions]


def safe_call(label, function, report):
    try:
        values = function()
        if not isinstance(values, tuple):
            raise TypeError('provider must return tuple')
        report[label] = {'status': 'OK', 'count': len(values), 'candidates': brief(values)}
        return values
    except Exception as exc:
        report[label] = {'status': 'ERROR', 'exception': type(exc).__name__, 'message': str(exc)}
        return ()


def cited_steps(bridge):
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    return tuple(link.step for link in bridge.proof_links
                 if link.step is not None and link.step.rule is ProofRule.GIVEN
                 and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                 and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content)


def compare(goal, bridge):
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
    from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
    from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization
    from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
    from phase165_r8_rule_provider import discover_inference_rules
    rules, catalog = discover_inference_rules()
    witnesses = cited_steps(bridge)
    available = tuple(s.conclusion for s in witnesses)
    record = {'reference_assertions': len(bridge.registry._assertions),
              'cited_witness_count': len(witnesses), 'rule_count': len(rules),
              'catalog_skipped_factories': list(catalog.skipped_factories), 'paths': {}}
    p = record['paths']
    safe_call('R26_GENERIC', lambda: build_generic_backward_expansion_provider(rules)(goal), p)
    safe_call('WITNESS_R2', lambda: reverse_rules_from_witnesses(goal, rules, witnesses), p)
    safe_call('SEEDED_R4', lambda: generate_seeded_backward_goals(goal, rules, witnesses), p)
    safe_call('CITED_SCALAR_SPECIALIZATION', lambda: expand_cited_general_specialization(goal, available), p)
    safe_call('ETA_SPECIALIZATION', lambda: expand_registered_eta_specialization(goal, available), p)
    safe_call('SHARED_NO_TARGET', lambda: shared_expansion_provider(bridge)(goal), p)
    safe_call('SHARED_WITH_TARGET', lambda: shared_expansion_provider(bridge, proof_target=goal)(goal), p)
    # Follow-up focused on the two independently forward-verified specialization routes.
    keys = ('R26_GENERIC','WITNESS_R2','SEEDED_R4','CITED_SCALAR_SPECIALIZATION',
            'ETA_SPECIALIZATION','SHARED_NO_TARGET','SHARED_WITH_TARGET')
    names = {key: [c['rule'] for c in p[key].get('candidates', [])] for key in keys}
    record['specialization_presence'] = {
        key: {'prop51': any('Proposition 5.1 generic higher-eta specialization' in n for n in names[key]),
              'cited_scalar': any('generic cited typed scalar specialization' in n for n in names[key]),
              'symmetry': any('equality symmetry' in n for n in names[key])}
        for key in keys}
    return record


def run():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    report = {'phase': '165 R6-2 R4-R11', 'status': 'PROVIDER_PATHS_AUDITED',
              'goals_found': len(goals), 'production_modified': False,
              'full_pytest_run': False, 'contexts': {}}
    if len(goals) != 1:
        report['status'] = 'GOAL_SELECTION_BLOCKED'
        report['goal_reprs'] = [repr(g) for g in goals]
        return report
    goal = goals[0]
    report['goal'] = repr(goal)
    context_id = next(iter(bridge.registry._assertions))
    report['contexts']['FULL'] = compare(goal, bridge)
    try:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id,
            verified_assertion_ids=())
        report['contexts']['SCREENED'] = compare(goal, screened)
    except Exception as exc:
        report['contexts']['SCREENED'] = {'status': 'ERROR',
            'exception': type(exc).__name__, 'message': str(exc)}
        report['status'] = 'SCREENING_ERROR'
    return report


def summary(report):
    return {'status': report['status'], 'goals_found': report['goals_found'],
            'contexts': {ctx: {'witnesses': value.get('cited_witness_count'),
                               'rules': value.get('rule_count'),
                               'counts': {k: v.get('count') for k,v in value.get('paths',{}).items()},
                               'path_errors': {k:v.get('message') for k,v in value.get('paths',{}).items() if v['status']=='ERROR'},
                               'specialization_presence': value.get('specialization_presence')}
                         for ctx,value in report['contexts'].items()},
            'production_modified': False, 'full_pytest_run': False}


def main():
    record = run()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'provider_paths.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    overview = summary(record)
    (OUT/'provider_paths.md').write_text('# R4-R11 Provider 経路比較\n\n```json\n'+json.dumps(overview,ensure_ascii=False,indent=2)+'\n```\n\n候補は証明済みの ProofStep ではありません。詳細は JSON を参照してください。\n', encoding='utf-8')
    print(json.dumps(overview, ensure_ascii=False, indent=2))
    if record['status'] != 'PROVIDER_PATHS_AUDITED':
        raise SystemExit(2)

if __name__ == '__main__':
    main()
