"""Read-only R50 runtime inspection of the existing finalization hook."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUTPUT = ROOT / 'phase165_r50_reason_loss_diagnostic_output'


def inspect_text(markdown: str) -> dict:
    paragraphs = markdown.split('\n\n')
    matches = []
    for index, paragraph in enumerate(paragraphs):
        if any(token in paragraph for token in ('\\Delta', '零写像', '単射性と全射性より', 'は全射', 'は単射', 'Im', 'ker')):
            matches.append({'index': index, 'text': paragraph[:900]})
    return {'length': len(markdown), 'paragraph_count': len(paragraphs), 'relevant_paragraphs': matches, 'has_Im': 'Im' in markdown, 'has_ker': 'ker' in markdown}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {'phase': '165 R50 reason-loss diagnostic', 'mode': 'READ_ONLY', 'events': [], 'status': 'error', 'production_files_modified': False, 'pytest_run': False}
    try:
        import toda_group_proof_narrative_contribution_renderer as contribution
        import phase165_r49_display_order as helper
        import toda_group_proof_narrative_reason_renderer as renderer
        from web_group_proof import build_standard_web_group_proof_view
        fn = getattr(contribution, 'finalize_phase165_r49_typed_reason_order', None)
        report['hook_in_contribution_module'] = fn is not None
        report['hook_points_to_helper'] = fn is getattr(helper, 'finalize_phase165_r49_typed_reason_order', None)
        if fn is None:
            raise RuntimeError('finalize_phase165_r49_typed_reason_order not imported in contribution module')
        original = fn
        def wrapped(markdown, reason_sidecar):
            event = {'stage': 'r49.finalize', 'before': inspect_text(markdown), 'reasons': []}
            for reason in reason_sidecar.reasons:
                item = {'kind': reason.kind.name, 'conclusion_type': type(reason.conclusion_step.conclusion).__name__, 'conclusion': repr(reason.conclusion_step.conclusion)[:450], 'premise_types': [type(p.conclusion).__name__ for p in reason.premise_steps]}
                try:
                    item['rendered_sentence'] = renderer.render_toda_group_proof_narrative_reason_sentence(reason)
                except Exception as exc:
                    item['renderer_error'] = repr(exc)
                event['reasons'].append(item)
            try:
                result = original(markdown, reason_sidecar)
                event['after'] = inspect_text(result)
                return result
            except Exception as exc:
                event['error'] = repr(exc)
                raise
            finally:
                report['events'].append(event)
        contribution.finalize_phase165_r49_typed_reason_order = wrapped
        try:
            view = build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode='narrative')
            markdown = '\n'.join(line.prefix + (line.statement_latex or '') + line.suffix for line in view.rendered_lines)
            report['web_output'] = inspect_text(markdown)
            report['web_references'] = markdown.split('使用する結果', 1)[1].split('証明', 1)[0] if '使用する結果' in markdown and '証明' in markdown else None
        finally:
            contribution.finalize_phase165_r49_typed_reason_order = original
        report['status'] = 'ok'
    except Exception as exc:
        report['error'] = repr(exc)
    (OUTPUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    event = report['events'][0] if report['events'] else {}
    lines = ['# Phase 165 R50 理由消失監査', '', f"- status: {report['status']}", f"- hook imported: {report.get('hook_in_contribution_module')}", f"- hook called: {bool(report['events'])}", f"- reason kinds: {[r['kind'] for r in event.get('reasons', [])]}", f"- before Im/ker: {event.get('before',{}).get('has_Im')}/{event.get('before',{}).get('has_ker')}", f"- after Im/ker: {event.get('after',{}).get('has_Im')}/{event.get('after',{}).get('has_ker')}", f"- Web Im/ker: {report.get('web_output',{}).get('has_Im')}/{report.get('web_output',{}).get('has_ker')}", '', '詳細は audit.json を参照。']
    (OUTPUT / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'hook_called': bool(report['events']), 'reason_kinds': [r['kind'] for r in event.get('reasons', [])], 'before_Im_ker': [event.get('before',{}).get('has_Im'),event.get('before',{}).get('has_ker')], 'after_Im_ker': [event.get('after',{}).get('has_Im'),event.get('after',{}).get('has_ker')], 'web_Im_ker': [report.get('web_output',{}).get('has_Im'),report.get('web_output',{}).get('has_ker')], 'output': str(OUTPUT / 'audit.json'), 'error': report.get('error')}, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'ok' else 1


if __name__ == '__main__':
    raise SystemExit(main())
