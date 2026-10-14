"""Phase 165 R27-R47: conservative orphan repository-module removal."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTECTED = frozenset({'proof_repository', 'standard_repository', 'unified_statement_registry'})


def dependency_edges(source: str) -> set[str]:
    tree = ast.parse(source)
    edges = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            edges.update(item.name.split('.')[0] for item in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            edges.add(node.module.split('.')[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {'import_module', '__import__'}:
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                edges.add(node.args[0].value.split('.')[0])
    return edges


def plan(root: Path) -> dict:
    sources = {}
    for path in sorted(root.glob('*.py')):
        if path.stem.startswith(('test_', 'audit_')) or '.phase' in path.stem or path.stem.endswith(('_backup', '_pre_cleanup')):
            continue
        sources[path.stem] = path.read_text(encoding='utf-8-sig')
    imports = {key: dependency_edges(value) & sources.keys() for key, value in sources.items()}
    legacy = {key for key in sources if key.startswith('repository_')}
    roots = set(sources) - legacy
    reachable = set(roots)
    pending = list(roots)
    while pending:
        for target in imports[pending.pop()]:
            if target not in reachable:
                reachable.add(target)
                pending.append(target)
    orphans = sorted(legacy - reachable)
    if PROTECTED.intersection(orphans):
        raise RuntimeError('Protected module unexpectedly classified as orphan')
    return {
        'orphan_modules': orphans,
        'remaining_legacy_modules': sorted(legacy & reachable),
        'active_legacy_imports': {
            key: sorted(imports[key] & legacy)
            for key in sorted(roots) if imports[key] & legacy
        },
        'critical_migration_pending': {
            key: sorted(imports.get(key, ()) & legacy)
            for key in ('toda_calculation', 'standard_production_applicability_catalog')
            if key in sources
        },
    }


def apply(root: Path = ROOT) -> dict:
    audit = plan(root)
    orphans = audit['orphan_modules']
    backup = root / 'phase165_r27_r47_backup'
    for name in orphans:
        original = root / f'{name}.py'
        previous = backup / original.name
        if previous.exists() and previous.read_bytes() != original.read_bytes():
            raise RuntimeError(f'Backup conflict: {previous}')
    if orphans:
        backup.mkdir(exist_ok=True)
        for name in orphans:
            original = root / f'{name}.py'
            previous = backup / original.name
            if not previous.exists():
                shutil.copy2(original, previous)
        for name in orphans:
            (root / f'{name}.py').unlink()
    audit.update({
        'phase': '165 R27-R47',
        'status': 'CHANGED' if orphans else 'NO_SAFE_CHANGES',
        'removed_legacy_modules': orphans,
        'legacy_catalog_unchanged': True,
        'legacy_group_calculation_unchanged': True,
        'full_pytest_run': False,
    })
    (root / 'phase165_r27_r47_audit.json').write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return audit


if __name__ == '__main__':
    apply()
