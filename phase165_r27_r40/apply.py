"""Phase 165 R27-R40: retire orphaned private Web legacy adapter helpers."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPERS = {
    'web_generator_exploration.py': ('_build_web_occurrence_view', '_build_web_occurrence_views', '_other_occurrence_presentations'),
    'web_generator_proof_scope.py': ('_toda_membership_match_labels', '_build_toda_membership_view', '_build_map_relation_view'),
    'web_generator_applicability.py': ('_build_rule_family_view', '_render_source_statement', '_build_source_view', '_build_source_views'),
    'web_generator_execution.py': ('_render_execution_statement',),
}
PRESERVE = frozenset(('proof_repository', 'standard_repository', 'unified_statement_registry',
    'phase163_r4_registry_bridge', 'phase165_r4_production_connection',
    'phase165_r9_production_wiring', 'phase165_r52_r5_auto_search',
    'toda_conclusion_latex_renderer'))


def remove_orphan_helpers(source: str, names: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    tree = ast.parse(source)
    candidates = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in names]
    present = {n.name for n in candidates}
    # Refuse partial local state: one of the expected helpers might have been intentionally replaced.
    if present != set(names):
        raise RuntimeError('Legacy helper signatures differ from expected: ' + str(set(names) - present))
    retained_nodes = [n for n in tree.body if n not in candidates]
    retained_tree = ast.Module(body=retained_nodes, type_ignores=[])
    retained_loads = {n.id for n in ast.walk(retained_tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    if any(name in retained_loads for name in names):
        raise RuntimeError('Cannot delete helper referenced by production code: ' + repr(sorted(set(names) & retained_loads)))
    lines = source.splitlines(keepends=True)
    for node in sorted(candidates, key=lambda n: n.lineno, reverse=True):
        begin = node.decorator_list[0].lineno - 1 if node.decorator_list else node.lineno - 1
        end = node.end_lineno
        lines[begin:end] = []
    changed = ''.join(lines)
    ast.parse(changed)
    return changed, tuple(sorted(present))


def prune_imports(source: str) -> tuple[str, tuple[str, ...]]:
    tree = ast.parse(source)
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    lines = source.splitlines(keepends=True)
    changes = []
    removed = []
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or not (node.module or '').startswith('repository_'):
            continue
        if any(alias.name == '*' for alias in node.names):
            continue
        keep = [a for a in node.names if (a.asname or a.name) in used]
        if len(keep) == len(node.names):
            continue
        removed.extend(node.module + '.' + a.name for a in node.names if a not in keep)
        replacement = ('from ' + node.module + ' import ' + ', '.join(a.name + (' as ' + a.asname if a.asname else '') for a in keep) + '\n') if keep else ''
        changes.append((node.lineno - 1, node.end_lineno, replacement))
    for begin, end, value in reversed(changes):
        lines[begin:end] = [value] if value else []
    changed = ''.join(lines)
    ast.parse(changed)
    return changed, tuple(removed)


def import_edges(text: str) -> set[str]:
    edges = set()
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            edges.update(alias.name.split('.')[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            edges.add(node.module.split('.')[0])
    return edges


def plan(root: Path, overrides: dict[str, str]) -> dict:
    sources = {}
    for path in sorted(root.glob('*.py')):
        if path.stem.startswith(('test_', 'audit_')) or '.phase' in path.stem or path.stem.endswith(('_backup', '_pre_cleanup')):
            continue
        sources[path.stem] = overrides.get(path.name, path.read_text(encoding='utf-8-sig'))
    imports = {key: import_edges(value) & sources.keys() for key, value in sources.items()}
    candidates = {name for name in sources if name.startswith('repository_')}
    reachable = set(sources) - candidates
    pending = list(reachable)
    while pending:
        for target in imports[pending.pop()]:
            if target not in reachable:
                reachable.add(target)
                pending.append(target)
    deletable = candidates - reachable
    if deletable & PRESERVE:
        raise RuntimeError('Protected module became deletable')
    return {
        'deletable': sorted(deletable),
        'retained_repository_modules': sorted(candidates & reachable),
        'reachable_from_non_repository': {key: sorted(value & candidates) for key, value in imports.items() if key not in candidates and value & candidates},
        'protected_core_present': sorted(PRESERVE & sources.keys()),
    }


def apply(root: Path = ROOT) -> dict:
    changed: dict[str, str] = {}
    helper_removals: dict[str, list[str]] = {}
    import_removals: dict[str, list[str]] = {}
    for name, helpers in HELPERS.items():
        path = root / name
        if not path.exists():
            raise FileNotFoundError(str(path))
        original = path.read_text(encoding='utf-8-sig')
        if all(not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == h for n in ast.parse(original).body) for h in helpers):
            continue  # Already applied.
        intermediate, removed_helpers = remove_orphan_helpers(original, helpers)
        result, removed_imports = prune_imports(intermediate)
        if result != original:
            changed[name] = result
            helper_removals[name] = list(removed_helpers)
            import_removals[name] = list(removed_imports)
    audit = plan(root, changed)
    paths = [root / name for name in changed] + [root / (name + '.py') for name in audit['deletable']]
    backup = root / 'phase165_r27_r40_backup'
    for path in paths:
        previous = backup / path.name
        if previous.exists() and previous.read_bytes() != path.read_bytes():
            raise RuntimeError('Backup conflict: ' + str(previous))
    if paths:
        backup.mkdir(exist_ok=True)
        for path in paths:
            previous = backup / path.name
            if not previous.exists():
                shutil.copy2(path, previous)
    for name, source in changed.items():
        (root / name).write_text(source, encoding='utf-8')
    for name in audit['deletable']:
        (root / (name + '.py')).unlink()
    audit.update({'phase': '165 R27-R40', 'status': 'CHANGED' if paths else 'NO_SAFE_CHANGES',
        'modified_files': sorted(changed), 'removed_private_helpers': helper_removals,
        'imports_removed': import_removals, 'full_pytest_run': False})
    (root / 'phase165_r27_r40_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return audit


if __name__ == '__main__':
    apply()
