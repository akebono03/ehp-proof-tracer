"""Phase 165 R5-R7: read-only reachability evidence for legacy Narrative routes."""
from __future__ import annotations

import ast
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'audit_output'

PUBLIC_ROOTS = ('web_group_proof.py', 'phase165_r52_r3_web_adapter.py', 'phase165_r52_partial_proof.py')
LEGACY_TARGETS = {
    'phase162_r3_narrative_connection.py': 'render_phase162_r3_narrative',
    'toda_group_proof_narrative_proof_chain_renderer.py': 'render_toda_group_proof_narrative_from_proof_chains_markdown',
    'toda_group_proof_narrative_concrete_transport.py': 'render_concrete_transport_proof_from_steps',
}
ADDITIONAL_ENTRY = 'phase162_web_narrative_integration.py'
CANONICAL = ('toda_group_proof_narrative_renderer.py', 'render_narrative_proof_model')


def sources(project: Path):
    """Only active top-level modules; never count snapshot .phase... files."""
    return sorted(p for p in project.glob('*.py') if '.phase' not in p.name and not p.name.startswith(('audit_', 'probe_')))


def scan(project: Path) -> dict:
    """Record module-level call edges; edges indicate possible, not certain execution."""
    files = sources(project)
    names = {p.stem: p.name for p in files}
    graph = {p.name: set() for p in files}
    calls = []
    parse_errors = []
    for p in files:
        try:
            tree = ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
        except SyntaxError as exc:
            parse_errors.append({'file': p.name, 'line': exc.lineno, 'message': str(exc)})
            continue
        imported_names = {}
        imported_modules = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in names:
                dst = names[node.module]
                for alias in node.names:
                    imported_names[alias.asname or alias.name] = (dst, alias.name)
                graph[p.name].add(dst)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in names:
                        dst = names[alias.name]
                        imported_modules[alias.asname or alias.name] = dst
                        graph[p.name].add(dst)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in imported_names:
                dst, name = imported_names[node.func.id]
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id in imported_modules:
                dst, name = imported_modules[node.func.value.id], node.func.attr
            else:
                continue
            calls.append({'source': p.name, 'target': dst, 'symbol': name, 'line': node.lineno})
    return {'graph': graph, 'calls': calls, 'parse_errors': parse_errors, 'scanned': len(files)}


def shortest_path(graph: dict[str, set[str]], start: str, end: str):
    if start not in graph or end not in graph:
        return None
    queue = deque([(start,)])
    visited = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == end:
            return list(path)
        for nxt in sorted(graph[path[-1]]):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((*path, nxt))
    return None


def analyze(project: Path):
    raw = scan(project)
    graph = raw['graph']
    targets = {}
    for target, function in LEGACY_TARGETS.items():
        direct = [r for r in raw['calls'] if r['target'] == target and r['symbol'] == function]
        paths = {r: shortest_path(graph, r, target) for r in PUBLIC_ROOTS}
        targets[target] = {
            'function': function,
            'direct_call_sites': direct,
            'public_import_paths': paths,
            'phase162_web_import_path': shortest_path(graph, ADDITIONAL_ENTRY, target),
            'has_public_import_path': any(path is not None for path in paths.values()),
        }
    canonical = {r: shortest_path(graph, r, CANONICAL[0]) for r in PUBLIC_ROOTS}
    old_web = {r: shortest_path(graph, r, ADDITIONAL_ENTRY) for r in PUBLIC_ROOTS}
    return {
        'phase': '165 R5-R7', 'status': 'REVIEW_REQUIRED',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'scanned_active_root_python': raw['scanned'],
        'parse_errors': raw['parse_errors'],
        'public_roots': list(PUBLIC_ROOTS),
        'canonical_module_paths': canonical,
        'old_phase162_web_paths': old_web,
        'legacy_targets': targets,
        'checks': {
            'no_syntax_errors': not raw['parse_errors'],
            'web_group_proof_reaches_canonical_module': canonical[PUBLIC_ROOTS[0]] is not None,
            'no_public_import_path_to_legacy_targets': not any(x['has_public_import_path'] for x in targets.values()),
            'no_public_import_path_to_phase162_web': all(x is None for x in old_web.values()),
        },
        'limitations': [
            'This is a conservative module-import graph, not a function-level runtime call graph.',
            'An import path is possible reachability, not evidence that a function executes.',
            'Absence of a path does not rule out dynamic imports, monkeypatches, route registration, or reflection.',
            'Static roots are restricted to the named Group Proof modules; CLI and other surfaces require separate review.',
            'No source code is modified. Historical Phase162 fixture failures remain unresolved.',
        ],
    }


def main():
    data = analyze(PROJECT)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'audit.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    lines = ['# Phase 165 R5-R7 公開到達経路監査', '', f"状態: **{data['status']}**", '', '## 静的検査', '']
    for name, result in data['checks'].items():
        lines.append(f"- {'PASS' if result else 'REVIEW' }: `{name}`")
    lines += ['', '## 公開入口から正規 Renderer への import 経路', '']
    for root, path in data['canonical_module_paths'].items():
        lines.append(f"- `{root}`: {' → '.join('`'+v+'`' for v in path) if path else '検出なし'}")
    lines += ['', '## 公開入口から旧 Phase 162 Web への import 経路', '']
    for root, path in data['old_phase162_web_paths'].items():
        lines.append(f"- `{root}`: {' → '.join('`'+v+'`' for v in path) if path else '検出なし'}")
    for file, info in data['legacy_targets'].items():
        lines += ['', f'## `{file}`', f"対象関数: `{info['function']}`", '', '### 直接呼び出し', '']
        lines += [f"- `{r['source']}:{r['line']}` → `{r['symbol']}`" for r in info['direct_call_sites']] or ['- 検出なし']
        lines += ['', '### 公開入口からの import 経路', '']
        for root, path in info['public_import_paths'].items():
            lines.append(f"- `{root}`: {' → '.join('`'+v+'`' for v in path) if path else '検出なし'}")
        path = info['phase162_web_import_path']
        lines += ['', f"旧 Phase 162 Web から: {' → '.join('`'+v+'`' for v in path) if path else '検出なし'}"]
    lines += ['', '## 限界', ''] + ['- '+x for x in data['limitations']]
    (OUT/'review.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps({'status': data['status'], 'checks': data['checks'],
                      'legacy_direct_call_counts': {k:len(v['direct_call_sites']) for k,v in data['legacy_targets'].items()},
                      'parse_errors': len(data['parse_errors']), 'report':str(OUT/'review.md'),
                      'full_pytest_run':False}, ensure_ascii=False, indent=2))
    if data['parse_errors']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
