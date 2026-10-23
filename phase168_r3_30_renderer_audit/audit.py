"""R3-30 read-only, deterministic source audit of the R3-29 narrative route."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'output'
TARGETS = {
    'renderer': 'phase168_r3_5_model_renderer.py',
    'narrative_model': 'phase168_r3_3_proof_narrative_model.py',
    'body_binding': 'phase168_r3_12_body_binding.py',
    'exactness': 'phase168_r3_26_exactness_projection.py',
    'typed': 'phase168_r3_27_typed_statement_projection.py',
    'order': 'phase168_r3_29_order_projection.py',
    'bridge': 'phase168_r3_4_link_bridge.py',
}

def audit_sources(root: Path = ROOT) -> dict:
    results = {}
    for role, name in TARGETS.items():
        f = root / name
        if not f.is_file():
            results[role] = {'file': name, 'exists': False}
            continue
        source = f.read_text(encoding='utf-8-sig')
        tree = ast.parse(source, filename=name)
        definitions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        imports = sorted({alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names} |
                         {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module})
        results[role] = {
            'file': name,
            'exists': True,
            'line_count': len(source.splitlines()),
            'definitions': [n.name for n in definitions],
            'imports': imports,
        }
        if role == 'renderer':
            fn = next((n for n in definitions if isinstance(n, ast.FunctionDef) and
                       n.name == 'render_model_backed_narrative_markdown'), None)
            if fn is None:
                results[role]['error'] = 'Public renderer function absent'
                continue
            calls = sorted({n.func.id if isinstance(n.func, ast.Name) else n.func.attr
                            for n in ast.walk(fn) if isinstance(n, ast.Call)
                            if isinstance(n.func, (ast.Name, ast.Attribute))})
            results[role].update({
                'function_lines': fn.end_lineno - fn.lineno + 1,
                'calls': calls,
                'references_citation_model': 'model.citations' in source and 'model.step_citation_numbers' in source,
                'uses_exactness_projection': 'project_exactness_chains' in calls,
                'uses_order_projection': 'project_narrative_order' in calls,
                'uses_typed_projection': 'typed_sentence' in calls,
                'reaches_legacy_renderer_by_direct_import': any('toda_group_proof_narrative' in x or 'toda_human_readable_renderer' in x for x in imports),
                'has_render_time_statement_type_checks': any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'isinstance' for n in ast.walk(fn)),
            })
    return {'status': 'AUDIT_ONLY', 'target': 'Phase 168 R3-29 post-install', 'sources': results,
            'limitations': [
                'This is a static audit; runtime dispatch and full Web entry wiring require separate runtime verification.',
                'No global proof-correctness or full-test-suite conclusion is inferred.',
                'Source version is read from the executing working tree, not from an earlier ZIP.',
            ]}

def report_markdown(report: dict) -> str:
    items = report['sources']
    lines = ['# Phase 168 R3-30 — Renderer 構造監査', '', '## 対象と結果', '']
    for role, info in items.items():
        lines.append(f"- {role}: `{info['file']}` — " +
                     (f"{info['line_count']} 行" if info['exists'] else 'ファイルなし'))
    lines += ['', '## Renderer の責務', '']
    renderer = items['renderer']
    if renderer.get('exists'):
        lines += [
            f"- 公開関数: {renderer.get('function_lines', '不明')} 行",
            f"- 完全列 Projection 呼出: {renderer.get('uses_exactness_projection', False)}",
            f"- 順序 Projection 呼出: {renderer.get('uses_order_projection', False)}",
            f"- 型付き Projection 呼出: {renderer.get('uses_typed_projection', False)}",
            f"- Reference の Model 経路: {renderer.get('references_citation_model', False)}",
            f"- 旧 Renderer への直接 import: {renderer.get('reaches_legacy_renderer_by_direct_import', False)}",
            f"- Renderer 内の型判定: {renderer.get('has_render_time_statement_type_checks', False)}",
        ]
    lines += ['', '## 注意', '']
    for limit in report['limitations']:
        lines.append('- ' + limit)
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    report = audit_sources()
    OUT.mkdir(exist_ok=True)
    (OUT / 'renderer_structure_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'renderer_structure_audit.md').write_text(report_markdown(report), encoding='utf-8')
    print(report_markdown(report))
    print('AUDIT_ONLY: no repository files modified')
