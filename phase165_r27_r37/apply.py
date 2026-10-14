"""Phase 165 R27-R37: safely prune unused legacy imports then batch sweep."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGETS = ('main.py', 'cli.py', 'web_generator_applicability.py',
           'web_generator_execution.py', 'web_generator_exploration.py',
           'web_generator_proof.py', 'web_generator_proof_scope.py',
           'web_operation_query.py', 'web_operation_query_proof.py',
           'web_group_proof.py', 'web_generator_proof.py',
           'web_generator_proof_scope.py', 'web_generator_applicability.py',
           'web_generator_execution.py', 'web_generator_exploration.py')
PROTECTED = frozenset(('proof_repository', 'standard_repository',
    'phase163_r4_registry_bridge', 'phase165_r4_production_connection',
    'phase165_r9_production_wiring', 'unified_statement_registry',
    'phase165_r52_r5_auto_search', 'repository_element_presentation'))


def imported_names_used(tree: ast.Module) -> set[str]:
    """Conservative: preserve names if referenced anywhere after import."""
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}


def prune_unused_legacy_imports(source: str) -> tuple[str, tuple[str, ...]]:
    tree = ast.parse(source)
    used = imported_names_used(tree)
    lines = source.splitlines(keepends=True)
    modifications = []
    removed = []
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or not (node.module or '').startswith('repository_'):
            continue
        # Keep all imports if the module is used by a wildcard import.
        if any(a.name == '*' for a in node.names):
            continue
        unused = [a for a in node.names if (a.asname or a.name) not in used]
        if not unused:
            continue
        remaining = [a for a in node.names if a not in unused]
        removed.extend(f'{node.module}.{a.name}' for a in unused)
        # Exact original AST span, no replacement of surrounding implementation.
        text = ''
        if remaining:
            names = ', '.join(a.name + (' as ' + a.asname if a.asname else '') for a in remaining)
            text = f'from {node.module} import {names}\n'
        modifications.append((node.lineno - 1, node.end_lineno, text))
    for start, end, value in reversed(modifications):
        lines[start:end] = [value] if value else []
    output = ''.join(lines)
    ast.parse(output)
    return output, tuple(removed)


def imports_of(source: str) -> set[str]:
    out = set()
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Import):
            out.update(a.name.split('.')[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module:
            out.add(n.module.split('.')[0])
    return out


def plan(root: Path, overrides: dict[str, str] | None = None) -> dict:
    overrides = overrides or {}
    sources = {}
    for p in sorted(root.glob('*.py')):
        if p.name.startswith(('test_', 'audit_')) or '.phase' in p.stem or p.stem.endswith(('_backup', '_pre_cleanup')):
            continue
        sources[p.stem] = overrides.get(p.name, p.read_text(encoding='utf-8-sig'))
    edges = {n: imports_of(s) & sources.keys() for n, s in sources.items()}
    candidates = {n for n in sources if n.startswith('repository_')}
    retained = set(sources) - candidates
    queue = list(retained)
    while queue:
        current = queue.pop()
        for dep in edges[current]:
            if dep not in retained:
                retained.add(dep)
                queue.append(dep)
    return {'deletable': sorted(candidates - retained),
            'retained_repository_modules': sorted(candidates & retained),
            'reachable_from_non_repository': {n: sorted(edges[n] & candidates) for n in sorted(sources.keys() - candidates) if edges[n] & candidates},
            'protected_core_present': sorted(PROTECTED & sources.keys())}


def apply(root: Path = ROOT) -> dict:
    updated = {}
    removed_imports = {}
    for name in TARGETS:
        path = root / name
        if not path.exists():
            continue
        original = path.read_text(encoding='utf-8-sig')
        after, removed = prune_unused_legacy_imports(original)
        if original != after:
            updated[name] = after
            removed_imports[name] = list(removed)
    result = plan(root, updated)
    # Check all changes before making any of them.
    backup = root / 'phase165_r27_r37_backup'
    paths = [root / n for n in updated] + [root / (n + '.py') for n in result['deletable']]
    for required in PROTECTED:
        if required in result['deletable']:
            raise RuntimeError('Protected module scheduled for deletion: ' + required)
    for path in paths:
        dest = backup / path.name
        if dest.exists() and dest.read_bytes() != path.read_bytes():
            raise RuntimeError('Backup conflict: ' + str(dest))
    if paths:
        backup.mkdir(exist_ok=True)
        for path in paths:
            dest = backup / path.name
            if not dest.exists():
                shutil.copy2(path, dest)
    for name, content in updated.items():
        (root / name).write_text(content, encoding='utf-8')
    for name in result['deletable']:
        (root / (name + '.py')).unlink()
    result.update({'phase': '165 R27-R37', 'status': 'CHANGED' if paths else 'NO_SAFE_CHANGES',
                   'imports_removed': removed_imports, 'modified_files': sorted(updated),
                   'full_pytest_run': False})
    (root / 'phase165_r27_r37_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

if __name__ == '__main__':
    apply()
