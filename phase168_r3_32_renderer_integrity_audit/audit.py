"""Read-only, focused renderer-integrity audit (no repository modifications)."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
OUT = Path(__file__).resolve().parent / 'output'
CASES = ((2, 1), (3, 1), (4, 1))
FILES = {
    'renderer': 'phase168_r3_5_model_renderer.py',
    'model': 'phase168_r3_3_proof_narrative_model.py',
    'binding': 'phase168_r3_12_body_binding.py',
    'exactness': 'phase168_r3_26_exactness_projection.py',
    'typed': 'phase168_r3_27_typed_statement_projection.py',
    'order': 'phase168_r3_29_order_projection.py',
}


def static_audit():
    data = {}
    suspicious = {'ProofStep', 'InferenceRule', 'GoalExpansion', 'create_legacy_given_proof_step', 'search_group_from_registered_goal'}
    for role, filename in FILES.items():
        source = (PROJECT / filename).read_text(encoding='utf-8')
        root = ast.parse(source)
        named_calls = sorted({node.func.id for node in ast.walk(root)
                              if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)})
        typed_checks = sorted({ast.unparse(node) for node in ast.walk(root)
                               if isinstance(node, ast.Call)
                               and isinstance(node.func, ast.Name) and node.func.id == 'isinstance'})
        data[role] = {
            'file': filename, 'lines': len(source.splitlines()),
            'isinstance_checks': typed_checks,
            'prohibited_constructor_or_search_calls': sorted(suspicious.intersection(named_calls)),
            'imports': sorted({alias.name for node in ast.walk(root)
                               if isinstance(node, ast.Import) for alias in node.names} |
                              {node.module for node in ast.walk(root)
                               if isinstance(node, ast.ImportFrom) and node.module}),
        }
    return data


def runtime_case(n, k):
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    before = (repr(result.proven_steps), repr(model.steps), repr(model.citations),
              repr(model.step_citation_numbers))
    markdown = render_model_backed_narrative_markdown(result, model)
    after = (repr(result.proven_steps), repr(model.steps), repr(model.citations),
             repr(model.step_citation_numbers))
    expected = [(c.number, c.reference.locator or c.reference.label) for c in model.citations]
    observed = [(int(num), heading) for num, heading in
                re.findall(r'^\*\*\[R(\d+)\] (.*?)\.\*\*\s*$', markdown, flags=re.M)]
    expected_marks = {int(x) for x in re.findall(r'\[R(\d+)\]', markdown)}
    known_marks = {c.number for c in model.citations}
    # A heading can be a literal with punctuation. Inspect the resulting list if mismatched.
    check = {
        'steps_equal': model.steps == result.proven_steps,
        'inputs_unchanged': before == after,
        'reference_headings_match_model': observed == expected,
        'every_reference_number_from_model': expected_marks <= known_marks,
        'citation_numbers_contiguous': sorted(known_marks) == list(range(1, len(model.citations) + 1)),
        'no_unresolved_fallback_label': 'fallback_type_name' not in markdown,
    }
    return {'group': f'pi_{n+k}^{n}', 'checks': check, 'pass': all(check.values()),
            'status': str(result.status), 'proof_steps': len(model.steps),
            'model_reference_count': len(expected), 'rendered_reference_count': len(observed),
            'expected_headings': expected, 'observed_headings': observed}


def main():
    static = static_audit()
    cases = []
    for n, k in CASES:
        try:
            cases.append(runtime_case(n, k))
        except Exception as exc:
            cases.append({'group': f'pi_{n+k}^{n}', 'pass': False,
                          'error': f'{type(exc).__name__}: {exc}'})
    clean = all(not entry['prohibited_constructor_or_search_calls'] for entry in static.values())
    passed = clean and all(item['pass'] for item in cases)
    output = {'status': 'PASS' if passed else 'REVIEW_REQUIRED', 'audit_only': True,
              'static': static, 'runtime': cases,
              'limitations': [
                  'A source-code scan does not establish mathematical soundness.',
                  'Runtime checks compare model-owned citations and step objects, not independent literature.',
                  'Only three registered goals are sampled, not all supported groups.',
                  'This does not inspect HTTP/browser routing or run the full pytest suite.',
              ]}
    OUT.mkdir(exist_ok=True)
    (OUT / 'renderer_integrity_audit.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    report = ['# Phase 168 R3-32 — Renderer 境界監査', '', f'判定: **{output["status"]}**', '',
              '## 実行時照合', '', '| 群 | 検証 | 証明ステップ | 引用数 |',
              '|---|---|---:|---:|']
    for c in cases:
        report.append(f'| {c["group"]} | {"PASS" if c["pass"] else "REVIEW_REQUIRED"} | '
                      f'{c.get("proof_steps", "-")} | {c.get("model_reference_count", "-")} |')
        if not c['pass']:
            report.append(f'\n詳細: `{json.dumps(c, ensure_ascii=False)}`\n')
    report.extend(['', '## Renderer の型判定', ''])
    report.extend('- '+check for check in static['renderer']['isinstance_checks'])
    report.extend(['', '## 限界', ''])
    report.extend('- '+s for s in output['limitations'])
    (OUT / 'renderer_integrity_audit.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    print('\n'.join(report))
    print('JSON:', OUT / 'renderer_integrity_audit.json')
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
