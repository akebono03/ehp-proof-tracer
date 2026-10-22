"""Phase 168 R2-11: same-invocation, read-only proof/reference trace."""
import argparse
import json
import sys
import traceback
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

STAGES = (
    'build_toda_group_proof_narrative_reference_entries',
    'filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary',
    '_select_toda_group_proof_narrative_reference_entries_and_statement_lines',
    'exclude_toda_group_proof_narrative_root_reference',
    'filter_toda_group_proof_narrative_reference_entries_by_body_usage',
    'restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage',
    'filter_toda_group_proof_narrative_reference_entries_by_step_usage',
    'prune_toda_group_proof_narrative_root_zero_direct_premise_references',
    'render_toda_group_proof_narrative_reference_entries_markdown',
)


def simple(value):
    return str(value)[:400]


def step_record(step, extractor):
    reference = extractor(step)
    rule = getattr(step, 'rule', None)
    inference_rule = getattr(step, 'inference_rule', None)
    return {
        'step_id': id(step),
        'rule': getattr(rule, 'name', simple(rule)),
        'inference_rule': getattr(inference_rule, 'name', None),
        'reference': getattr(reference, 'locator', None),
        'reference_label': getattr(reference, 'label', None),
        'premises': [id(x) for x in (getattr(step, 'premises', None) or ())],
        'conclusion_type': type(getattr(step, 'conclusion', None)).__name__,
        'conclusion_repr': repr(getattr(step, 'conclusion', None))[:400],
    }


def entry_records(entries):
    return [
        {'number': getattr(x, 'number', None),
         'locator': getattr(getattr(x, 'reference', None), 'locator', None),
         'label': getattr(getattr(x, 'reference', None), 'label', None),
         'step_ids': [id(s) for s in getattr(x, 'proof_steps', ())]}
        for x in entries
    ]


def entries_from_result(stage, result):
    if stage == 'render_toda_group_proof_narrative_reference_entries_markdown':
        return None
    candidate = result[0] if stage in (
        '_select_toda_group_proof_narrative_reference_entries_and_statement_lines',
        'exclude_toda_group_proof_narrative_root_reference',
        'filter_toda_group_proof_narrative_reference_entries_by_body_usage',
        'restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage',
        'filter_toda_group_proof_narrative_reference_entries_by_step_usage',
        'prune_toda_group_proof_narrative_root_zero_direct_premise_references',
    ) else result
    if not isinstance(candidate, (tuple, list)):
        return None
    if candidate and not hasattr(candidate[0], 'reference'):
        return None
    return entry_records(candidate)


def run():
    import toda_group_proof_narrative_contribution_renderer as renderer
    import toda_group_proof_narrative_references as refs
    from web_group_proof import build_standard_web_group_proof_view

    events = []
    presentations = []
    active_depth = [0]
    original_render = renderer.render_toda_group_proof_narrative_multi_argument_with_contributions_markdown

    def traced_render(presentation, *args, **kwargs):
        presentations.append(presentation)
        active_depth[0] += 1
        try:
            return original_render(presentation, *args, **kwargs)
        finally:
            active_depth[0] -= 1

    patches = [patch.object(renderer, 'render_toda_group_proof_narrative_multi_argument_with_contributions_markdown', traced_render)]
    for stage in STAGES:
        original = getattr(renderer, stage)
        def wrap(*args, _original=original, _stage=stage, **kwargs):
            if not active_depth[0]:
                return _original(*args, **kwargs)
            before = entry_records(args[0]) if args and isinstance(args[0], (list, tuple)) and (not args[0] or hasattr(args[0][0], 'reference')) else None
            event = {'ordinal': len(events) + 1, 'stage': _stage, 'before': before}
            events.append(event)
            try:
                output = _original(*args, **kwargs)
                event['after'] = entries_from_result(_stage, output)
                if _stage == 'render_toda_group_proof_narrative_reference_entries_markdown':
                    event['reference_section'] = output
                if _stage == 'filter_toda_group_proof_narrative_reference_entries_by_body_usage':
                    event['markdown_has_R_marker'] = '[R' in args[2] if len(args) > 2 and isinstance(args[2], str) else None
                return output
            except Exception as exc:
                event['error'] = repr(exc)
                raise
        patches.append(patch.object(renderer, stage, wrap))

    for p in patches:
        p.start()
    error = None
    view = None
    try:
        view = build_standard_web_group_proof_view(2, 2, 2, 'narrative')
    except Exception:
        error = traceback.format_exc()
    finally:
        for p in reversed(patches):
            p.stop()

    trees = []
    for presentation in presentations:
        nodes = [step_record(node.proof_step, refs.extract_toda_group_proof_step_literature_reference) for node in presentation.nodes]
        root = presentation.root_step
        by_id = {x['step_id']: x for x in nodes}
        used = set()
        def visit(step):
            sid = id(step)
            if sid in used:
                return
            used.add(sid)
            for premise in getattr(step, 'premises', ()) or ():
                visit(premise)
        visit(root)
        trees.append({'root_step_id': id(root), 'node_count': len(nodes), 'reachable_step_ids': sorted(used),
                      'reachable_locators': sorted({x['reference'] for x in nodes if x['step_id'] in used and x['reference']}),
                      'nodes': nodes, 'missing_reachable_nodes': sorted(used - set(by_id))})

    public = {'key': getattr(view, 'key', None), 'rendered_lines': []}
    if view is not None:
        for line in getattr(view, 'rendered_lines', ()):
            public['rendered_lines'].append({'kind': getattr(line, 'kind', None), 'prefix': simple(getattr(line, 'prefix', '')),
                                             'statement_latex': simple(getattr(line, 'statement_latex', '')),
                                             'suffix': simple(getattr(line, 'suffix', ''))})
    return {'audit': 'phase168_r2_11', 'target': 'pi_4^2', 'call': 'build_standard_web_group_proof_view(2,2,2,"narrative")',
            'presentations': trees, 'events': events, 'public': public, 'error': error,
            'limitations': ['instrumented contribution renderer path only', 'if no presentation captured inspect public route',
                            'source output reflects local working tree; no files modified']}


def report(data):
    lines = ['# Phase 168 R2-11 Proof Tree / Reference 実行時監査', '', '対象: $\\pi_4^2$、単一 Web 呼び出し、読み取り専用', '',
             f"- presentation 捕捉数: {len(data['presentations'])}", f"- Reference 処理イベント: {len(data['events'])}",
             f"- Web view key: `{data['public']['key']}`", '']
    for i, tree in enumerate(data['presentations'], 1):
        lines += [f'## Proof Tree #{i}', '', f"- nodes: {tree['node_count']}",
                  f"- reachable nodes: {len(tree['reachable_step_ids'])}",
                  '- reachable Reference: ' + (', '.join(tree['reachable_locators']) or '(なし)'),
                  f"- reachable nodes not present in presentation.nodes: {len(tree['missing_reachable_nodes'])}", '']
    lines += ['## Reference 処理イベント（同一呼び出し内）', '', '| # | stage | before | after |', '|---:|---|---|---|']
    for ev in data['events']:
        def fmt(xs):
            return '—' if xs is None else ', '.join(f"{x['number']}:{x['locator']}" for x in xs) or '(empty)'
        lines.append(f"| {ev['ordinal']} | `{ev['stage']}` | {fmt(ev['before'])} | {fmt(ev.get('after'))} |")
    lines += ['', '## Public Reference section', '']
    inside = False
    for line in data['public']['rendered_lines']:
        if line['kind'] == 'heading' and line['prefix'] == '使用する結果':
            inside = True
            continue
        if inside and line['kind'] == 'heading' and line['prefix'] == '証明':
            break
        if inside:
            lines.append(' '.join(str(line.get(k) or '') for k in ('prefix', 'statement_latex', 'suffix')))
    if data['error']:
        lines += ['', '## 実行エラー', '', '```', data['error'], '```']
    lines += ['', '## 監査上の注意', '', 'これは文献採否の変更・修正ではありません。実行経路が捕捉できない場合も成功扱いにせず、原因を分析してください。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(Path(__file__).resolve().parent / 'output'))
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    try:
        data = run()
    except Exception:
        data = {'audit': 'phase168_r2_11', 'presentations': [], 'events': [], 'public': {'key': None, 'rendered_lines': []}, 'error': traceback.format_exc()}
    (out / 'proof_reference_trace.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'proof_reference_trace.md').write_text(report(data), encoding='utf-8')
    print('AUDIT_ONLY: no repository files modified')
    print('PRESENTATIONS:', len(data['presentations']))
    print('EVENTS:', len(data['events']))
    print('REPORT:', out / 'proof_reference_trace.md')
    print('JSON:', out / 'proof_reference_trace.json')
    if data['error']:
        print('RUNTIME_ERROR: see report')
        return 2
    if not data['presentations']:
        print('NO_PRESENTATION_CAPTURED: inspect Web routing')
        return 3
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
