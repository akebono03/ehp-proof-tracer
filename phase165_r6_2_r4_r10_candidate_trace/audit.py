"""R4-R10: read-only candidate-to-ProofStep trace for pi_4^3."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = Path(__file__).resolve().parent / 'audit_output'


def classify_root(rule_name: str) -> str:
    if 'generic higher-eta specialization' in rule_name:
        return 'PROP51_SPECIALIZATION'
    if 'generic cited typed scalar specialization' in rule_name:
        return 'CITED_SCALAR_SPECIALIZATION'
    if 'equality symmetry' in rule_name:
        return 'SYMMETRY'
    return 'OTHER'


def trace(bridge, goal, provider, context_id):
    import phase165_r3_recursive_search as canonical
    from proof import ProofRule
    original = canonical.find_inference_matches_for_rule
    calls = []
    observations = []
    provider_events = []

    def traced_match(rule, premises):
        found = tuple(original(rule, premises))
        calls.append({'rule': getattr(rule, 'name', repr(rule)),
                      'premises': [repr(x.conclusion) for x in premises],
                      'premise_rules': [str(x.rule) for x in premises],
                      'matching_inference_count': len(found)})
        return found

    def observed_provider(target):
        result = provider(target)
        provider_events.append({'goal': repr(target), 'candidate_count': len(result),
                                'candidates': [{'rule': getattr(x.rule, 'name', repr(x.rule)),
                                                'kind': classify_root(getattr(x.rule, 'name', '')),
                                                'subgoals': [repr(g) for g in x.subgoals]}
                                               for x in result]})
        return result

    def observer(kind, target, step):
        observations.append({'kind': kind, 'goal': repr(target),
                             'step_rule': str(step.rule) if step else None,
                             'inference_rule': getattr(step.inference_rule, 'name', None) if step else None})

    canonical.find_inference_matches_for_rule = traced_match
    try:
        try:
            step = canonical.reconstruct_registered_goal(
                goal, bridge, context_id, observed_provider,
                lookup_mode='typed_reference', progress_observer=observer)
            result = {'status': 'CANONICAL_COMPLETE', 'root_step': True,
                      'root_rule': str(step.rule), 'root_inference_rule': getattr(step.inference_rule, 'name', None)}
        except canonical.RegisteredGoalUnresolved as exc:
            result = {'status': 'CANONICAL_UNRESOLVED', 'root_step': False, 'diagnostic': str(exc)}
        except Exception as exc:
            result = {'status': 'EXECUTION_ERROR', 'root_step': False, 'error_type': type(exc).__name__, 'error': str(exc)}
    finally:
        canonical.find_inference_matches_for_rule = original
    result.update({'provider_events': provider_events, 'inference_match_calls': calls, 'observations': observations})
    return result


def run():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider, search_shared_group_goal
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_partial_proof import ProofSearchStatus
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    report = {'phase': '165 R6-2 R4-R10', 'status': 'CANDIDATE_TRACE_AUDITED',
              'goal_count': len(goals), 'assertions': len(bridge.registry._assertions),
              'production_modified': False, 'full_pytest_run': False, 'traces': {}}
    if len(goals) != 1:
        report['status'] = 'GOAL_SELECTION_BLOCKED'
        return report
    goal = goals[0]
    context_id = next(iter(bridge.registry._assertions))
    contexts = {'full_bridge': bridge}
    try:
        contexts['screened_bridge'] = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id, verified_assertion_ids=())
    except Exception as exc:
        report['screening_error'] = {'type': type(exc).__name__, 'message': str(exc)}
    for name, selected in contexts.items():
        provider = shared_expansion_provider(selected, proof_target=goal)
        roots = provider(goal)
        report['traces'][name] = {'root_candidates': [
            {'index': i + 1, 'rule': getattr(x.rule, 'name', repr(x.rule)),
             'kind': classify_root(getattr(x.rule, 'name', '')),
             'subgoals': [repr(s) for s in x.subgoals]}
            for i, x in enumerate(roots)], 'all': trace(selected, goal, provider, context_id)}
        for i, root in enumerate(roots):
            def single_at_root(target, chosen=root):
                if type(target) is type(goal) and target == goal:
                    return (chosen,)
                return provider(target)
            report['traces'][name][f'root_{i+1}'] = trace(selected, goal, single_at_root, context_id)
    for name, fn in (
        ('shared_direct', lambda: search_shared_group_goal(n=3, k=1, group_structure=goal.rhs, bridge=bridge)),
        ('web_search', lambda: search_group_from_registered_goal(n=3, k=1, bridge=bridge)),
    ):
        try:
            value = fn()
            report[name] = {'status': str(value.status), 'complete': value.status is ProofSearchStatus.COMPLETE,
                            'proven_steps': len(value.proven_steps), 'diagnostics': list(value.diagnostics)}
        except Exception as exc:
            report[name] = {'status': 'ERROR', 'error': str(exc), 'type': type(exc).__name__}
    return report


def summary(report):
    return {'status': report['status'], 'goal_count': report['goal_count'],
            'traces': {name: {'root_candidate_count': len(data['root_candidates']),
                              'all_status': data['all']['status'],
                              'root_statuses': [data[f'root_{i+1}']['status'] for i in range(len(data['root_candidates']))],
                              'match_calls': len(data['all']['inference_match_calls'])}
                       for name, data in report['traces'].items()},
            'shared_direct': report.get('shared_direct'), 'web_search': report.get('web_search'),
            'production_modified': False, 'full_pytest_run': False}


def main():
    result = run()
    OUT.mkdir(exist_ok=True)
    (OUT/'candidate_trace.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    overview = summary(result)
    lines = ['# R4-R10 候補から ProofStep までの追跡', '', '候補数・前提の解決・推論照合・採用の各段階を調査します。', '', '```json', json.dumps(overview, ensure_ascii=False, indent=2), '```', '',
             '詳細は candidate_trace.json を参照してください。', '', '監査は既存 API を呼び、ファイルを書き換えません。実行中の関数置換は finally 節で復元します。',
             'ルートを1候補に絞る診断は本番の選択方針を変更するものではありません。', '全体 pytest は実行していません。']
    (OUT/'candidate_trace.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(overview, ensure_ascii=False, indent=2))
    if result['status'] != 'CANDIDATE_TRACE_AUDITED':
        raise SystemExit(2)

if __name__ == '__main__':
    main()
