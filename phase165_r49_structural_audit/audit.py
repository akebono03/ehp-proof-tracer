from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    'toda_group_proof_narrative_reasons.py',
    'toda_group_proof_narrative_reason_renderer.py',
    'web_group_proof.py',
    'phase165_goal_only_search.py',
]
KEYWORDS = ('DeltaZero', 'DeltaInjective', 'Isomorphism', 'EXACTNESS_TO_MAP_PROPERTY', 'ReasonSidecar', 'reason_sidecar', 'MapInjective', 'MapSurjective')
report = {'phase': '165 R49', 'mode': 'READ_ONLY_STRUCTURAL_AUDIT', 'files': {}, 'tests': [], 'production_files_modified': False, 'full_pytest_run': False}
for name in FILES:
    p = ROOT / name
    if not p.exists():
        report['files'][name] = {'present': False}
        continue
    source = p.read_text(encoding='utf-8-sig')
    try:
        tree = ast.parse(source)
        definitions = [{'name': node.name, 'line': node.lineno, 'kind': type(node).__name__} for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        error = None
    except SyntaxError as exc:
        definitions = []
        error = str(exc)
    matches = [{'line': i, 'text': line.strip()[:200]} for i, line in enumerate(source.splitlines(), 1) if any(x in line for x in KEYWORDS)]
    report['files'][name] = {'present': True, 'syntax_error': error, 'definitions': definitions, 'matches': matches[:250]}
for base in (ROOT / 'tests', ROOT):
    if not base.is_dir():
        continue
    for p in sorted(base.glob('test*reason*.py')):
        report['tests'].append(str(p.relative_to(ROOT)))
report['tests'] = sorted(set(report['tests']))
outdir = ROOT / 'phase165_r49_audit_output'
outdir.mkdir(exist_ok=True)
(outdir / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
lines = ['# Phase 165 R49 構造監査', '', '現行コードの定義・呼出し箇所を収集した読み取り専用監査です。実装修正、数学的検証、pytest は行っていません。', '']
for name, obj in report['files'].items():
    lines += [f'## {name}', f'存在: {obj["present"]}', '']
    if obj['present']:
        lines += [f'構文エラー: {obj["syntax_error"]}', '### 関連行']
        lines += [f'- {r["line"]}: `{r["text"]}`' for r in obj['matches']]
        lines += ['', '### 定義']
        lines += [f'- {d["kind"]} {d["name"]}: {d["line"]}' for d in obj['definitions']]
    lines += ['']
lines += ['## 関連テスト候補'] + [f'- `{t}`' for t in report['tests']]
(outdir / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(json.dumps({'phase': report['phase'], 'mode': report['mode'], 'report': str(outdir / 'report.md'), 'production_files_modified': False, 'full_pytest_run': False}, ensure_ascii=False, indent=2))
