"""Phase 168 R2-12: read-only active Web path audit for pi_4^2."""
from __future__ import annotations
import json
import sys
import traceback
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def safe(value):
    try:
        return repr(value)[:600]
    except Exception as exc:
        return '<repr error: ' + type(exc).__name__ + '>'


def step_record(step, ref_extract=None):
    ir = getattr(step, 'inference_rule', None)
    ref = getattr(ir, 'literature_reference', None)
    if ref_extract is not None:
        try:
            ref = ref_extract(step)
        except Exception as exc:
            ref = 'EXTRACTION_ERROR: ' + str(exc)
    return {
        'identity': id(step), 'rule': str(getattr(step, 'rule', None)),
        'conclusion': safe(getattr(step, 'conclusion', None)),
        'inference_rule': getattr(ir, 'name', None),
        'reference': safe(ref) if ref is not None else None,
        'premise_ids': [id(s) for s in getattr(step, 'premises', ())],
    }


def report():
    import web_group_proof
    import phase165_r55_nk_only_goal as goal_module
    import phase165_r52_partial_proof as partial
    import phase165_r56_presentation_adapter as adapter
    import toda_group_proof_narrative_renderer as narrative
    import toda_group_proof_narrative_references as references
    import toda_group_proof_narrative_contribution_renderer as contributions

    events = []
    state = {'result': None, 'presentation': None}
    original_search = goal_module.search_group_from_registered_goal
    original_build = adapter.build_toda_group_proof_presentation
    original_render = adapter.render_toda_group_proof_narrative_markdown
    original_entries = references.build_toda_group_proof_narrative_reference_entries
    original_entries_local = contributions.build_toda_group_proof_narrative_reference_entries

    def searched(*args, **kwargs):
        result = original_search(*args, **kwargs)
        state['result'] = result
        events.append({'stage': 'SEARCH_RESULT', 'status': str(result.status), 'steps': len(result.proven_steps), 'references': list(result.references)})
        return result

    def built(*args, **kwargs):
        presentation = original_build(*args, **kwargs)
        state['presentation'] = presentation
        events.append({'stage': 'PRESENTATION', 'nodes': len(presentation.nodes), 'root': id(presentation.root_step)})
        return presentation

    def extracted(presentation):
        entries = original_entries(presentation)
        events.append({'stage': 'REFERENCE_BUILT', 'entries': [dict(number=e.number, reference=safe(e.reference), step_ids=[id(s) for s in e.proof_steps]) for e in entries]})
        return entries

    def rendered(presentation):
        events.append({'stage': 'NARRATIVE_ENTRY', 'root': id(presentation.root_step)})
        return original_render(presentation)

    with patch.object(goal_module, 'search_group_from_registered_goal', searched), \
         patch.object(adapter, 'build_toda_group_proof_presentation', built), \
         patch.object(adapter, 'render_toda_group_proof_narrative_markdown', rendered), \
         patch.object(references, 'build_toda_group_proof_narrative_reference_entries', extracted), \
         patch.object(contributions, 'build_toda_group_proof_narrative_reference_entries', extracted):
        view = web_group_proof.build_standard_web_group_proof_view(2, 2, 2, 'narrative')

    result = state['result']
    presentation = state['presentation']
    output = {
        'audit': 'phase168_r2_12', 'target': 'pi_4^2',
        'call': 'build_standard_web_group_proof_view(2,2,2,"narrative")',
        'events': events,
        'web': {'key': view.key, 'rendered_lines': [dict(kind=x.kind, prefix=x.prefix, statement_latex=x.statement_latex, suffix=x.suffix) for x in view.rendered_lines]},
        'result': None if result is None else {
            'status': str(result.status), 'references': list(result.references),
            'proven_steps': [step_record(s, references.extract_toda_group_proof_step_literature_reference) for s in result.proven_steps],
            'conclusion': safe(result.conclusion),
        },
        'presentation': None if presentation is None else {
            'root_id': id(presentation.root_step),
            'nodes': [step_record(n.proof_step, references.extract_toda_group_proof_step_literature_reference) for n in presentation.nodes],
        },
        'limitations': ['read-only monkey patches in current process', 'does not establish correctness of mathematical proof', 'runtime captures only the recorded entry points'],
    }
    return output


def main():
    folder = Path(__file__).resolve().parent / 'output'
    folder.mkdir(parents=True, exist_ok=True)
    try:
        data = report()
    except Exception as exc:
        data = {'audit': 'phase168_r2_12', 'error': repr(exc), 'traceback': traceback.format_exc()}
    (folder / 'active_route_trace.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 168 R2-12 実行経路監査', '', '本番コード無変更。対象: $\\pi_4^2$。', '']
    if 'error' in data:
        lines.extend(['## ERROR', '', '```', data['traceback'], '```'])
    else:
        lines.extend(['## 観測イベント', ''])
        for e in data['events']:
            lines.append('- ' + e['stage'] + ': ' + json.dumps(e, ensure_ascii=False))
        lines.extend(['', '## 検索結果', '', 'Status: ' + str(data['result']['status'] if data['result'] else 'NOT_CAPTURED'), 'Proof steps: ' + str(len(data['result']['proven_steps']) if data['result'] else 0), 'Presentation nodes: ' + str(len(data['presentation']['nodes']) if data['presentation'] else 0), '', '## Web 表示', ''])
        for line in data['web']['rendered_lines']:
            lines.append('- ' + ' '.join(str(line[k] or '') for k in ('prefix', 'statement_latex', 'suffix')))
    (folder / 'active_route_trace.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('AUDIT_ONLY: no repository files modified')
    print('EVENTS:', len(data.get('events', [])))
    print('PRESENTATION_NODES:', len((data.get('presentation') or {}).get('nodes', [])))
    print('REPORT:', folder / 'active_route_trace.md')
    print('JSON:', folder / 'active_route_trace.json')
    if 'error' in data:
        print('AUDIT_ERROR:', data['error'])
        return 1
    if data.get('presentation') is None:
        print('NO_PRESENTATION_CAPTURED: verify completed adapter routing')
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
