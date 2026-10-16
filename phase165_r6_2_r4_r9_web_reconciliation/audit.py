"""Read-only reconciliation of canonical, partial and Web proof paths."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = Path(__file__).resolve().parent / 'audit_output'


def capture_result(result: Any) -> dict[str, Any]:
    return {
        'status': str(getattr(result, 'status', 'UNKNOWN')),
        'conclusion': repr(getattr(result, 'conclusion', None)),
        'proven_step_count': len(getattr(result, 'proven_steps', ())),
        'proved_conclusions': [repr(x.conclusion) for x in getattr(result, 'proven_steps', ())],
        'step_rules': [str(x.rule) for x in getattr(result, 'proven_steps', ())],
        'open_goals': [repr(x) for x in getattr(result, 'open_goals', ())],
        'diagnostics': list(getattr(result, 'diagnostics', ())),
        'references': list(getattr(result, 'references', ())),
    }


def safe_stage(name, function):
    try:
        return {'stage': name, 'ok': True, 'value': function()}
    except Exception as exc:
        return {'stage': name, 'ok': False, 'error_type': type(exc).__name__, 'error': str(exc)}


def run() -> dict[str, Any]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_renderer_narrative_model import build_narrative_proof_model
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=1)
    report = {
        'phase': '165 R6-2 R4-R9', 'status': 'WEB_CANONICAL_RECONCILIATION_AUDITED',
        'target_count': len(targets), 'targets': [repr(t) for t in targets],
        'registry_assertions': len(bridge.registry._assertions),
        'proof_links': len(bridge.proof_links), 'stages': {},
        'production_modified': False, 'full_pytest_run': False,
    }
    if len(targets) != 1:
        report['status'] = 'BLOCKED_GOAL_SELECTION'
        return report
    goal = targets[0]
    stages = report['stages']
    # Normal Web search entry: includes reviewed proof order and context screening.
    stage = safe_stage('web_search_entry', lambda: search_group_from_registered_goal(n=3, k=1, bridge=bridge))
    if stage['ok']:
        result = stage.pop('value')
        stage['result'] = capture_result(result)
        stage['complete'] = result.status is ProofSearchStatus.COMPLETE
        view = safe_stage('partial_web_adapter', lambda: build_partial_web_group_proof_view(result, max_depth=2, mode='narrative'))
        if view['ok']:
            val = view.pop('value')
            view['summary'] = {'partial_result': val.partial_result, 'step_count': len(val.steps), 'rendered_line_count': len(val.rendered_lines),
                               'rendered_text': [str(getattr(x, 'text', x)) for x in val.rendered_lines]}
        stages['partial_web_adapter'] = view
        model = safe_stage('narrative_model', lambda: build_narrative_proof_model(result))
        if model['ok']:
            val = model.pop('value')
            model['summary'] = {'status': str(val.status), 'step_count': len(val.proven_steps), 'root_step_present': val.root_step is not None, 'source_kind': val.source_kind}
        stages['narrative_model'] = model
    stages['web_search_entry'] = stage
    direct = safe_stage('shared_direct_no_order', lambda: search_shared_group_goal(n=3, k=1, group_structure=goal.rhs, bridge=bridge))
    if direct['ok']:
        result = direct.pop('value')
        direct['result'] = capture_result(result)
        direct['complete'] = result.status is ProofSearchStatus.COMPLETE
    stages['shared_direct_no_order'] = direct
    native = safe_stage('public_web_entry', lambda: build_standard_web_group_proof_view(3, 1, max_depth=2, mode='narrative'))
    if native['ok']:
        val = native.pop('value')
        native['summary'] = {'partial_result': val.partial_result, 'step_count': len(val.steps), 'rendered_line_count': len(val.rendered_lines), 'key': val.key,
                             'rendered_text': [str(getattr(x, 'text', x)) for x in val.rendered_lines]}
    stages['public_web_entry'] = native
    try:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
        catalog, diagnostic = resolve_reviewed_order_catalog(bridge, n=3, k=1)
        stages['proof_order'] = {'ok': True, 'diagnostic': diagnostic, 'catalog_type': type(catalog).__name__ if catalog is not None else None}
    except Exception as exc:
        stages['proof_order'] = {'ok': False, 'error_type': type(exc).__name__, 'error': str(exc)}
    return report


def render_md(report: dict[str, Any]) -> str:
    lines = ['# R4-R9 正規探索・Web 結果照合', '', f"状態: `{report['status']}`", '',
             f"目標候補: {report['target_count']}、型付き主張: {report['registry_assertions']}、リンク: {report['proof_links']}", '']
    for key, stage in report['stages'].items():
        lines.extend([f'## {key}', '', f"- 呼出成功: {stage['ok']}"])
        if not stage['ok']:
            lines.append(f"- 例外: `{stage['error_type']}` — {stage['error']}")
        if 'complete' in stage:
            lines.append(f"- 完成: {stage['complete']}")
        if 'result' in stage:
            result = stage['result']
            lines.extend([f"- 状態: {result['status']}", f"- ProofStep: {result['proven_step_count']}",
                          f"- 診断: {result['diagnostics']}", f"- 未解決: {len(result['open_goals'])}"])
        if 'summary' in stage:
            lines.append(f"- 概要: `{str({k:v for k,v in stage['summary'].items() if k!='rendered_text'})}`")
        if key == 'proof_order':
            lines.append(f"- 利用順序診断: {stage.get('diagnostic')}")
        lines.append('')
    lines.extend(['## 判定の限界', '', 'この監査は既存の実行経路の出力を照合するのみで、証明済みの結論や Reference を新規生成しません。',
                  '各呼出の検証条件や表示内容が一致したことをもって数学的証明の成立を追加認定しません。',
                  '全体 pytest は実行していません。'])
    return '\n'.join(lines)+'\n'


def main():
    report = run()
    OUT.mkdir(exist_ok=True)
    (OUT/'web_canonical_reconciliation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT/'web_canonical_reconciliation.md').write_text(render_md(report), encoding='utf-8')
    summary = {'status': report['status'], 'target_count': report['target_count'], 'stages': {k: {'ok':v['ok'], 'complete':v.get('complete'), 'diagnostics':v.get('result',{}).get('diagnostics')} for k,v in report['stages'].items()}, 'production_modified': False, 'full_pytest_run': False}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report['status'] != 'WEB_CANONICAL_RECONCILIATION_AUDITED':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
