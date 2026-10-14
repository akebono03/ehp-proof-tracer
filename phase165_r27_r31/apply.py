"""Phase 165 R27-R31: conservative batch deletion of unreachable legacy repository modules."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
PROTECTED = frozenset({
    'proof_repository', 'standard_repository', 'phase163_r4_registry_bridge',
    'phase165_r4_production_connection', 'phase165_r9_production_wiring',
    'unified_statement_registry', 'phase165_r52_r5_auto_search',
})


def imports_of(source: str) -> set[str]:
    tree = ast.parse(source)
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split('.')[0])
    return found


def plan(root: Path) -> dict:
    sources = {}
    for path in sorted(root.glob('*.py')):
        if path.name.startswith('test_') or path.name.startswith('audit_'):
            continue
        sources[path.stem] = path.read_text(encoding='utf-8-sig')
    edges = {name: imports_of(source) & sources.keys() for name, source in sources.items()}
    candidates = {name for name in sources if name.startswith('repository_')}
    retained = set(sources) - candidates
    queue = list(retained)
    while queue:
        module = queue.pop()
        for dep in edges[module]:
            if dep not in retained:
                retained.add(dep)
                queue.append(dep)
    deletable = sorted(candidates - retained)
    return {
        'deletable': deletable,
        'retained_repository_modules': sorted(candidates & retained),
        'protected_core_present': sorted(x for x in PROTECTED if x in sources),
        'reachable_from_non_repository': {name: sorted(set(edges[name]) & candidates) for name in sorted(sources.keys() - candidates) if edges[name] & candidates},
    }


def apply(root: Path = ROOT, package: Path = PACKAGE) -> dict:
    result = plan(root)
    backup = root / 'phase165_r27_r31_removed_backup'
    for name in result['deletable']:
        source = root / (name + '.py')
        if not source.exists():
            raise RuntimeError('File disappeared during deletion: ' + str(source))
    for name in result['deletable']:
        backup.mkdir(exist_ok=True)
        source = root / (name + '.py')
        dest = backup / source.name
        if dest.exists() and dest.read_bytes() != source.read_bytes():
            raise RuntimeError('Backup conflict: ' + str(dest))
        if not dest.exists():
            shutil.copy2(source, dest)
    for name in result['deletable']:
        (root / (name + '.py')).unlink()
    result.update(phase='165 R27-R31', status='REMOVED' if result['deletable'] else 'NO_SAFE_DELETIONS', full_pytest_run=False)
    (root / 'phase165_r27_r31_audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == '__main__':
    apply()
