"""Phase 165 R27-R30: bulk, dependency-guarded retirement of legacy builders."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

PHASE = '165 R27-R30'
PATCHES = {
    'phase163_r4_r12_stable_bases.py': (
        'existing_stable_minimal_registration',
        'def existing_stable_minimal_registration() -> StableBaseRegistration:\n'
        '    """Retired: historical proof-builder extraction is not typed registration."""\n'
        '    raise RuntimeError("Legacy Bootstrap-derived stable-base extraction retired; supply typed source assertions explicitly")\n',
    ),
    'phase163_r4_r13_inventory.py': (
        'existing_phase163_r4_r13_inventory',
        'def existing_phase163_r4_r13_inventory() -> InventoryReport:\n'
        '    """Retired: historical proof-builder extraction is not typed inventory."""\n'
        '    raise RuntimeError("Legacy Bootstrap-derived inventory extraction retired; use registered typed assertion snapshots")\n',
    ),
}
PRIMARY_TARGET = 'toda_upstream_bootstrap.py'
PROTECTED = {
    'proof_repository.py', 'phase164_r8_proofstep_factory.py',
    'phase165_r52_r5_auto_search.py', 'phase165_r9_production_wiring.py',
    'unified_statement_registry.py', 'toda_rules.py',
}


def replace_function(source: str, name: str, replacement: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(found) != 1:
        raise RuntimeError(f'Expected one {name}; found {len(found)}')
    node = found[0]
    assert isinstance(node, ast.FunctionDef)
    if ast.dump(node, include_attributes=False) == ast.dump(ast.parse(replacement).body[0], include_attributes=False):
        return source, False
    lines = source.splitlines(keepends=True)
    nl = '\r\n' if '\r\n' in source else '\n'
    updated = ''.join(lines[:node.lineno-1]) + replacement.replace('\n', nl) + ''.join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated, True


def import_references(source: str, filename: str) -> list[tuple[str, int, str]]:
    tree = ast.parse(source, filename=filename)
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            result.append((node.module.split('.')[0], node.lineno, 'import'))
        elif isinstance(node, ast.Import):
            result.extend((alias.name.split('.')[0], node.lineno, 'import') for alias in node.names)
    return result


def candidate_names(root: Path) -> set[str]:
    # Limit deletion to explicitly named legacy builder families.
    return {
        p.name for p in root.glob('toda_*bootstrap.py')
        if p.name not in PROTECTED
    } | {
        p.name for p in root.glob('standard_production_repository.py')
    }


def plan(root: Path) -> dict:
    root_files = sorted(root.glob('*.py'))
    replacements = {}
    for file, (function, replacement) in PATCHES.items():
        path = root / file
        if not path.is_file():
            raise RuntimeError(f'Missing required module: {file}')
        previous = path.read_text(encoding='utf-8-sig')
        updated, changed = replace_function(previous, function, replacement)
        if changed:
            replacements[file] = updated
    candidates = candidate_names(root)
    all_sources = {
        p.name: replacements.get(p.name, p.read_text(encoding='utf-8-sig'))
        for p in root_files
    }
    root_edges = []
    for file, source in all_sources.items():
        for imported, line, kind in import_references(source, file):
            target = imported + '.py'
            if target in candidates:
                root_edges.append({'source': file, 'target': target, 'line': line, 'kind': kind})
    # Retain anything imported by any noncandidate module; then retain
    # dependencies of those retained candidates. Delete only isolated islands.
    retained = set()
    blockers = []
    for edge in root_edges:
        if edge['source'] not in candidates:
            retained.add(edge['target'])
            blockers.append(edge)
    while True:
        newly_retained = {e['target'] for e in root_edges if e['source'] in retained}
        if newly_retained <= retained:
            break
        retained |= newly_retained
    deletable = sorted(candidates - retained)
    if PRIMARY_TARGET in candidates and PRIMARY_TARGET not in deletable:
        # Do not silently claim this core target is retired.
        raise RuntimeError('Upstream bootstrap still referenced: ' + json.dumps([e for e in root_edges if e['target'] == PRIMARY_TARGET], ensure_ascii=False))
    return {
        'replacements': replacements,
        'deletable': deletable,
        'retained': sorted(retained),
        'references': blockers,
        'candidates': sorted(candidates),
    }


def apply(root: Path | None = None) -> dict:
    root = Path.cwd() if root is None else Path(root)
    audit_path = root / 'phase165_r27_r30_audit.json'
    p = plan(root)
    changes = [root / name for name in p['replacements']]
    deleted_paths = [root / name for name in p['deletable']]
    backups = root / 'phase165_r27_r30_removed_backup'
    for item in changes + deleted_paths:
        previous = backups / item.name
        if previous.exists() and previous.read_bytes() != item.read_bytes():
            raise RuntimeError(f'Backup conflict: {item.name}; no changes made')
    if changes or deleted_paths:
        backups.mkdir(exist_ok=True)
        for item in changes + deleted_paths:
            shutil.copy2(item, backups / item.name)
    for name, source in p['replacements'].items():
        (root / name).write_text(source, encoding='utf-8')
    for path in deleted_paths:
        path.unlink()
    result = {
        'phase': PHASE,
        'status': 'REMOVED' if deleted_paths else 'ALREADY_REMOVED_OR_BLOCKED',
        'deleted': p['deletable'],
        'retained_bootstraps': p['retained'],
        'protected_core': sorted(PROTECTED),
        'registration_helpers_changed': sorted(p['replacements']),
        'blocking_imports': p['references'],
        'full_pytest_run': False,
    }
    audit_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
