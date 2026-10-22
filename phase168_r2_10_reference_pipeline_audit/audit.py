from __future__ import annotations
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'output'
OUT.mkdir(exist_ok=True)
FILES = {
    'renderer': ROOT / 'toda_group_proof_narrative_contribution_renderer.py',
    'references': ROOT / 'toda_group_proof_narrative_references.py',
}
TESTS = [
    'tests/test_phase167_r2_unified_reference.py',
    'tests/test_phase167_r2_shared_reference.py',
    'tests/test_phase157_r4_r3_reference_selection_integration.py',
    'tests/test_phase157_r4_r3_repair1_reference_retention.py',
    'tests/test_phase153_r3_3_reference_statement_selection.py',
    'tests/test_phase164_r2_citation_eligibility.py',
]
KEYWORDS = ('reference', 'citation', 'root', 'body_usage', 'step_usage', 'fixed_statement', 'restore', 'prune')

def full_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return full_name(node.value) + '.' + node.attr
    return ''

def calls(node):
    return [(full_name(c.func), c.lineno) for c in ast.walk(node) if isinstance(c, ast.Call)]

def nearest_function(tree, line):
    matches = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.lineno <= line <= n.end_lineno]
    return min(matches, key=lambda n: n.end_lineno - n.lineno).name if matches else '<module>'

def inspect(path):
    source = path.read_text(encoding='utf-8-sig')
    tree = ast.parse(source, filename=str(path))
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(k in node.name.lower() for k in KEYWORDS):
                functions.append({'function': node.name, 'start': node.lineno, 'end': node.end_lineno,
                                  'reference_calls': [{'function': name, 'line': line} for name, line in calls(node)
                                                      if any(k in name.lower() for k in KEYWORDS)]})
    return source, tree, sorted(functions, key=lambda x: x['start'])

def main():
    missing = [str(p) for p in FILES.values() if not p.is_file()]
    if missing:
        raise SystemExit('Missing required files: ' + ', '.join(missing))
    data = {'scope': 'static read-only audit; local working tree', 'files': {}, 'pipeline': [], 'test_inventory': [], 'warnings': []}
    for label, path in FILES.items():
        source, tree, functions = inspect(path)
        data['files'][label] = {'path': str(path.relative_to(ROOT)), 'lines': len(source.splitlines()), 'functions': functions}
        if label == 'renderer':
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for fn, line in calls(node):
                    if any(k in fn.lower() for k in KEYWORDS) and any(word in fn.lower() for word in ('reference', 'citation')):
                        data['pipeline'].append({'caller': node.name, 'line': line, 'callee': fn})
            data['pipeline'].sort(key=lambda x: x['line'])
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    expression = ast.get_source_segment(source, node.test) or ''
                    if '[R' in expression or 'rendered' in expression and 'reference' in expression:
                        data['warnings'].append({'file': str(path.name), 'line': node.lineno,
                                                 'function': nearest_function(tree, node.lineno),
                                                 'condition': expression, 'category': 'text-dependent citation decision'})
        for f in functions:
            name = f['function'].lower()
            if 'body_usage' in name or 'step_usage' in name or 'restore' in name:
                data['warnings'].append({'file': path.name, 'line': f['start'], 'function': f['function'],
                                         'category': 'candidate proof/text reconciliation (review manually)'})
    for relative in TESTS:
        p = ROOT / relative
        if p.exists():
            source, tree, _ = inspect(p)
            functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]
            data['test_inventory'].append({'path': relative, 'tests': functions})
        else:
            data['test_inventory'].append({'path': relative, 'missing': True})
    (OUT / 'reference_pipeline.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    md = ['# Phase 168 R2-10 Reference pipeline 静的監査', '',
          '監査対象: ローカル作業ツリー。**コードは変更しない**。この監査は AST に基づき、実行時の件数を確定するものではない。', '',
          '## Renderer に現れる参照関数呼び出し（行番号順）', '',
          '| 行 | 所属関数 | 呼び出し |', '|---:|---|---|']
    for item in data['pipeline']:
        md.append(f"| {item['line']} | `{item['caller']}` | `{item['callee']}` |")
    md.extend(['', '## テキスト依存・再判定候補', '', '| ファイル:行 | 関数 | 分類・条件 |', '|---|---|---|'])
    for w in data['warnings']:
        md.append(f"| `{w['file']}:{w['line']}` | `{w['function']}` | {w['category']}: `{w.get('condition', '')}` |")
    md.extend(['', '## 関連テスト', ''])
    for t in data['test_inventory']:
        md.append(f"- `{t['path']}` — " + ('ファイルなし' if t.get('missing') else ', '.join(t['tests'])))
    md.extend(['', '## 判定原則（設計提案、現状事実ではない）', '',
               '1. Proof Tree の実依存から GIVEN と INFERENCE の文献出典を収集する。',
               '2. 掲載順・自己参照の妥当性は Search 側で保証する。',
               '3. 同一文献を統合後、番号・本文引用・Reference セクションを一貫生成する。',
               '4. `"[R" in rendered` 等の Markdown 文字列から採否を逆判定しない。',
               '5. 実動作の確認には同じ presentation と同じ呼び出しで段階ごとの ID/件数を観測する。', '',
               '## 制限', '',
               '- AST 静的検査であり、分岐の実行条件・参照の正当性は自動確定しない。',
               '- GitHub の develop とローカルツリーが異なる場合、結果はローカル側に基づく。',
               '- π₄² の Reference 2件は目標値であり、実測として宣言しない。', ''])
    (OUT / 'reference_pipeline_report.md').write_text('\n'.join(md), encoding='utf-8')
    print('AUDIT_ONLY: no repository files modified')
    print('PIPELINE_CALLS:', len(data['pipeline']))
    print('REVIEW_CANDIDATES:', len(data['warnings']))
    print('REPORT:', OUT / 'reference_pipeline_report.md')
    print('JSON:', OUT / 'reference_pipeline.json')

if __name__ == '__main__':
    main()
