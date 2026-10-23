"""Read-only runtime audit: proof steps, model projection, renderer, baseline."""
from __future__ import annotations
import json
import hashlib
import re
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_12_body_binding import build_narrative_body_lines
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof_common import _group_proof_statement_latex

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGETS = ((2, 1, 'pi3_2'), (3, 1, 'pi4_3'), (4, 1, 'pi5_4'), (2, 2, 'pi4_2'))


def run_one(n: int, k: int, name: str) -> dict:
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    body = build_narrative_body_lines(result, model)
    printed_indices = {line.step_index for line in body}
    markdown = render_model_backed_narrative_markdown(result, model)
    steps = []
    for index, step in enumerate(model.steps):
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        steps.append({
            'index': index,
            'type': type(step.conclusion).__name__,
            'rule': str(step.rule),
            'inference': getattr(step.inference_rule, 'name', None),
            'premise_count': len(step.premises),
            'citation_numbers': list(model.step_citation_numbers[index]),
            'latex': latex,
            'fallback_type': fallback,
            'generic_body_included': index in printed_indices,
            'rendered_exact_statement': bool(latex and '$' + latex + '$' in markdown),
        })
    references = [{
        'number': item.number,
        'locator': item.reference.locator or item.reference.label,
        'step_indices': list(item.step_indices),
        'assertion_ids': list(item.assertion_ids),
        'reference_ids': list(item.reference_ids),
    } for item in model.citations]
    baseline_file = PACKAGE / 'baselines' / (name + '_original.txt')
    historical = baseline_file.read_text(encoding='utf-8-sig') if baseline_file.exists() else None
    markers = {
        'pi3_2': ['単射', '零写像', '全射', '同型', 'H(\\eta_{2})'],
        'pi4_3': ['\\operatorname{Im}\\Delta', '\\ker E', '全射', '準同型定理', 'E(\\eta_{2})'],
        'pi5_4': ['(n,m,k)=(3,4,1)', 'は同型', 'E\\eta_{3}'],
        'pi4_2': ['Proposition 5.1', '(5.2)'],
    }[name]
    def normalized(text):
        return re.sub(r'\s+', '', text or '').replace('\\left', '').replace('\\right', '')
    gaps = [{'marker': marker, 'in_baseline': marker in normalized(historical),
             'in_new': marker in normalized(markdown)} for marker in markers]
    return {
        'group': name, 'n': n, 'k': k,
        'search_status': str(result.status),
        'model_root_index': model.root_index,
        'proof_step_count': len(model.steps),
        'generic_body_count': len(body),
        'generic_body_skipped_count': len(model.steps) - len(body),
        'unrenderable_step_types': sorted({s['type'] for s in steps if not s['generic_body_included']}),
        'references': references,
        'steps': steps,
        'baseline_sha256': hashlib.sha256(baseline_file.read_bytes()).hexdigest() if baseline_file.exists() else None,
        'historical_markers': gaps,
        'model_markdown': markdown,
        'baseline_text': historical,
    }


def main():
    output = PACKAGE / 'output'
    output.mkdir(exist_ok=True)
    report = {'read_only': True, 'targets': [], 'errors': []}
    for n, k, name in TARGETS:
        try:
            item = run_one(n, k, name)
            report['targets'].append(item)
            (output / (name + '_new.md')).write_text(item['model_markdown'], encoding='utf-8')
            print(f"{name}: steps={item['proof_step_count']} generic_body={item['generic_body_count']} skipped={item['generic_body_skipped_count']}")
            for m in item['historical_markers']:
                print(' ', m['marker'], 'old=', m['in_baseline'], 'new=', m['in_new'])
        except Exception as exc:
            report['errors'].append({'target': name, 'type': type(exc).__name__, 'message': str(exc)})
            print('ERROR', name, type(exc).__name__, str(exc))
    (output / 'runtime_gap_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    summary = ['# Phase 168 証明文章の実行時ギャップ監査', '', '本監査は読み取り専用。基準文章の Reference 番号は固定しない。', '']
    for item in report['targets']:
        summary += [f"## {item['group']}", f"- 検索状態: {item['search_status']}", f"- 証明ステップ: {item['proof_step_count']}、通常数式化: {item['generic_body_count']}、除外: {item['generic_body_skipped_count']}", '- 除外された型: ' + ', '.join(item['unrenderable_step_types']), '- 比較印: ' + '; '.join(f"{x['marker']} (元:{x['in_baseline']}, 新:{x['in_new']})" for x in item['historical_markers']), '']
    if report['errors']:
        summary += ['## 実行時エラー', json.dumps(report['errors'], ensure_ascii=False, indent=2)]
    (output / 'summary.md').write_text('\n'.join(summary) + '\n', encoding='utf-8')
    print('REPORT:', output / 'runtime_gap_report.json')
    if report['errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
