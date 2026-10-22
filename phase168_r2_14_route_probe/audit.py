from __future__ import annotations
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'output'
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))


def preview(value):
    if value is None:
        return None
    return str(value)[:240]


def run():
    import toda_group_proof_narrative_renderer as narrative
    import toda_group_proof_narrative_contribution_renderer as contributions
    from web_group_proof import build_standard_web_group_proof_view
    events = []
    captures = {}

    def attach(module, name, stack):
        original = getattr(module, name)
        def wrapped(*args, **kwargs):
            entry = {'stage': name, 'level': 'enter', 'root_rule': preview(getattr(getattr(args[0], 'root_step', None), 'inference_rule', None).name) if args and getattr(getattr(args[0], 'root_step', None), 'inference_rule', None) else None}
            events.append(entry)
            try:
                value = original(*args, **kwargs)
            except Exception as exc:
                events.append({'stage': name, 'level': 'error', 'error': repr(exc)})
                raise
            events.append({'stage': name, 'level': 'exit', 'result_type': type(value).__name__, 'length': len(value) if isinstance(value, str) else None, 'has_references': '使用する結果' in value if isinstance(value,str) else None, 'has_auxiliary': '補助結果' in value if isinstance(value,str) else None})
            if isinstance(value, str):
                captures[name] = value
            return value
        stack.append(patch.object(module, name, wrapped))

    from contextlib import ExitStack
    with ExitStack() as stack:
        patches = []
        for module, name in ((narrative, '_phase160_r7_render_stable_finite_cyclic_transport_narrative'),
                             (narrative, '_phase160_r7_previous_public_narrative_renderer'),
                             (narrative, '_phase158_baseline_render_toda_group_proof_narrative_markdown'),
                             (narrative, 'render_toda_group_proof_narrative_multi_argument_with_contributions_markdown'),
                             (contributions, 'render_toda_group_proof_narrative_multi_argument_with_contributions_markdown')):
            if hasattr(module, name):
                attach(module, name, patches)
        for p in patches:
            stack.enter_context(p)
        try:
            view = build_standard_web_group_proof_view(2, 2, 2, 'narrative')
            public = [{'kind': line.kind, 'prefix': line.prefix, 'statement_latex': line.statement_latex, 'suffix': line.suffix} for line in view.rendered_lines]
            error = None
        except Exception as exc:
            public = []
            error = repr(exc)
    result = {'target': 'pi_4^2', 'events': events, 'public': public, 'error': error,
              'captured_markdown': captures,
              'notes': ['A wrapper event proves invocation; missing event does not prove source function absence.',
                        'No repository files are modified.',
                        'R2-13 local modifications, if present, are evaluated as-is.']}
    (OUT / 'route_trace.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    md = ['# Phase 168 R2-14 実行経路監査', '', '対象: $\\pi_4^2$。本番コードは変更しない。', '', '## 経路']
    for e in events:
        md.append('- ' + ' / '.join(str(e.get(k)) for k in ('stage','level','has_references','has_auxiliary')))
    md += ['', '## Web 出力', '']
    for p in public:
        md.append('- ' + ' '.join(str(p.get(k) or '') for k in ('prefix','statement_latex','suffix')))
    md += ['', '## エラー', '', str(error), '', '## 判定', '',
           '共通 Contribution Renderer の enter が無い場合、手前の分岐・別名束縛を優先して確認する。',
           'enter がある場合は exit の有無と has_references の変化を確認する。']
    (OUT / 'route_trace.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    print('AUDIT_ONLY: no repository files modified')
    print('EVENTS:', len(events))
    print('CONTRIBUTION_ENTER:', sum(e.get('level')=='enter' and 'contributions_markdown' in e.get('stage','') for e in events))
    print('ERROR:', error)
    print('JSON:', OUT / 'route_trace.json')
    print('REPORT:', OUT / 'route_trace.md')
    return 0 if error is None else 2

if __name__ == '__main__':
    raise SystemExit(run())
