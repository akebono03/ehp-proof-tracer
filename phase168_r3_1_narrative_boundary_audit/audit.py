from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent / 'output'
OUT.mkdir(parents=True, exist_ok=True)
FILES = (
    'web_group_proof.py',
    'phase165_r52_r3_web_adapter.py',
    'phase165_r55_nk_only_goal.py',
    'phase165_r52_r9_shared_math.py',
    'toda_group_proof_narrative_contribution_renderer.py',
    'toda_group_proof_narrative_references.py',
    'toda_group_proof_narrative_renderer.py',
    'toda_group_proof_narrative.py',
)
SIGNALS = (
    'reference', 'render', 'narrative', 'search', 'proof_tree',
    'proof_step', 'root', 'body_usage', 'step_usage', 'literature',
)

def analyze_file(name: str) -> dict:
    file = ROOT / name
    if not file.is_file():
        return {'path': name, 'present': False}
    source = file.read_text(encoding='utf-8-sig')
    tree = ast.parse(source, filename=name)
    functions = []
    for item in ast.walk(tree):
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(s in item.name.lower() for s in SIGNALS):
            continue
        calls = []
        for node in ast.walk(item):
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name):
                    calls.append(fn.id)
                elif isinstance(fn, ast.Attribute):
                    calls.append(fn.attr)
        functions.append({'name': item.name, 'line': item.lineno,
                          'end_line': item.end_lineno,
                          'calls_of_interest': sorted(set(c for c in calls if any(s in c.lower() for s in SIGNALS)))})
    return {'path': name, 'present': True, 'lines': len(source.splitlines()),
            'functions': sorted(functions, key=lambda f: f['line'])}

def main() -> None:
    result = {'kind': 'READ_ONLY_STATIC_AUDIT', 'files': [analyze_file(n) for n in FILES]}
    tests = []
    for f in sorted(ROOT.rglob('test*.py')):
        if len(f.relative_to(ROOT).parts) > 5:
            continue
        if any(part.startswith('.') for part in f.relative_to(ROOT).parts):
            continue
        name = str(f.relative_to(ROOT)).replace('\\', '/')
        if any(s in name.lower() for s in ('reference', 'narrative', 'web_group', 'phase168_r2')):
            tests.append(name)
    result['related_test_candidates'] = tests[:250]
    result['notes'] = [
        'Static calls indicate candidates, not runtime reachability.',
        'No repository code, documentation, or tests are modified.',
        'Proof Tree content and citation extraction require subsequent runtime validation.',
    ]
    target = OUT / 'boundary_audit.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 168 R3-1 境界監査', '', '本監査は静的解析のみ。実行経路の確定ではありません。', '']
    for entry in result['files']:
        lines.append(f"## {entry['path']}")
        if not entry['present']:
            lines.append('ファイルなし')
            continue
        lines.append(f"{entry['lines']} lines; relevant functions: {len(entry['functions'])}")
        for fn in entry['functions']:
            lines.append(f"- {fn['line']}-{fn['end_line']}: `{fn['name']}` => {', '.join(fn['calls_of_interest'])}")
        lines.append('')
    lines.extend(['## 関連テスト候補', *['- `' + x + '`' for x in tests[:250]]])
    (OUT / 'boundary_audit.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('AUDIT_ONLY: no repository files modified')
    print('JSON:', target)
    print('MARKDOWN:', OUT / 'boundary_audit.md')

if __name__ == '__main__':
    main()
