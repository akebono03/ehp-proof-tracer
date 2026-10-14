"""Phase 165 R27-R59: conservative bulk retirement with reversible archival."""
from __future__ import annotations
import ast
import json
import zipfile
from pathlib import Path

PHASE = '165 R27-R59-R1'
ROOT = Path(__file__).resolve().parent.parent
OLD = frozenset({'toda_calculation', 'toda_calculation_report',
                  'repository_foundational_group_specialization', 'repository_proof_scope',
                  'repository_symbolic_sigma_specialization', 'repository_symbolic_stable_group_specialization'})
FACADE = 'toda_calculation_facade'
OLD_API = frozenset({'build_toda_report', 'build_standard_toda_report'})
PROTECTED = frozenset({'main.py', 'cli.py', 'web_group_query.py', 'web_group_proof.py',
                       'toda_typed_group_facade.py', 'phase165_r52_r5_auto_search.py',
                       'toda_calculation_facade.py'})


def deps(source: str) -> set[str]:
    result = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module.split('.')[0])
        elif isinstance(node, ast.Import):
            result.update(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.Call) and node.args:
            f = node.func
            if (isinstance(f, ast.Name) and f.id in ('__import__', 'import_module') or
                isinstance(f, ast.Attribute) and f.attr == 'import_module'):
                if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    result.add(node.args[0].value.split('.')[0])
    return result


def remove_legacy_facade_api(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    edits = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in OLD_API:
            edits.append((node.lineno, node.end_lineno))
    if {node.name for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in OLD_API} != OLD_API:
        # Idempotence: already removed is acceptable, half-removed is not.
        if not any(isinstance(n, ast.FunctionDef) and n.name in OLD_API for n in tree.body):
            return source
        raise RuntimeError('Partial legacy facade API; manual review required')
    for start, end in reversed(edits):
        del lines[start - 1:end]
    updated = ''.join(lines)
    tree2 = ast.parse(updated)
    loaded = {n.id for n in ast.walk(tree2) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    removals = []
    for n in tree2.body:
        if not isinstance(n, ast.ImportFrom) or not n.module:
            continue
        if n.module in {'toda_calculation_report', 'standard_production_repository',
                        'phase164_r7_repository_root_resolution', 'proof_repository',
                        'toda_calculation_report_result', 'toda_group_query'} and all(
                            (a.asname or a.name) not in loaded for a in n.names):
            removals.append((n.lineno, n.end_lineno))
    lines = updated.splitlines(keepends=True)
    for start, end in reversed(removals):
        del lines[start - 1:end]
    updated = ''.join(lines)
    ast.parse(updated)
    return updated


def source_paths(root: Path):
    yield from sorted(root.glob('*.py'))
    if (root / 'tests').is_dir():
        yield from sorted((root / 'tests').rglob('test_*.py'))


def plan(root: Path) -> dict:
    root = Path(root)
    facade = root / (FACADE + '.py')
    if not facade.is_file():
        raise RuntimeError('Missing facade')
    old_src = facade.read_text(encoding='utf-8-sig')
    new_src = remove_legacy_facade_api(old_src)
    if OLD_API & {n.name for n in ast.walk(ast.parse(new_src)) if isinstance(n, ast.FunctionDef)}:
        raise RuntimeError('Old API still present')
    if 'build_standard_toda_partial_result' not in new_src:
        raise RuntimeError('Typed partial facade entry is absent; refusing removal')
    preexisting = {p.stem for p in source_paths(root)}
    old_present = sorted(OLD & preexisting)
    blocked = {}
    direct_tests = {}
    historical_scripts = {}
    for path in source_paths(root):
        relative = path.relative_to(root).as_posix()
        if path.stem in OLD or path.name == facade.name:
            continue
        source = path.read_text(encoding='utf-8-sig')
        importset = deps(source)
        legacy_imports = sorted(importset & OLD)
        # Explicit use of legacy facade API including from-import or module.attribute.
        old_symbols = sorted(x for x in OLD_API if x in source)
        if not legacy_imports and not old_symbols:
            continue
        data = {'old_imports': legacy_imports, 'old_api_symbols': old_symbols}
        if relative.startswith('tests/'):
            direct_tests[relative] = data
        elif relative in PROTECTED or (path.stem in {'toda_calculation_report_result', 'toda_calculation_result'}):
            blocked[relative] = data
        else:
            historical_scripts[relative] = data
    for target in ('toda_typed_group_facade.py', 'phase165_r52_r5_auto_search.py'):
        if not (root/target).is_file():
            blocked[target] = {'missing': True}
        else:
            source = (root/target).read_text(encoding='utf-8-sig')
            if deps(source) & (OLD | {FACADE}):
                blocked[target] = {'typed_entry_depends_on_legacy': sorted(deps(source) & (OLD | {FACADE}))}
    # Archive self-contained historical audit scripts, not live library modules.
    archival_scripts = {}
    root_modules = {p.stem: p for p in root.glob('*.py')}
    root_imports = {p.stem: deps(p.read_text(encoding='utf-8-sig'))
                    for p in root.glob('*.py') if p.stem not in OLD}
    for relative, data in historical_scripts.items():
        module = Path(relative).stem
        if relative.startswith('audit_') or relative.startswith('test_phase') or relative == 'phase162_r4_b3_web_common_display.py':
            archival_scripts[relative] = data
        else:
            blocked[relative] = data
    # A historical script cannot be archived if still imported by active code.
    # Scan every top-level module, not only the formerly protected list.
    archived_modules = {Path(p).stem for p in archival_scripts}
    for rel in archival_scripts:
        module = Path(rel).stem
        consumers = sorted(name for name, uses in root_imports.items()
                           if module in uses and name not in archived_modules and name not in OLD)
        if consumers:
            blocked[rel] = {'still_imported_by': consumers}
    # Tests sometimes import helper functions from tests that are being retired.
    # Include these dependents transitively; do not break remaining test collection.
    tests_dir = root / 'tests'
    if tests_dir.is_dir():
        test_sources = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8-sig')
                        for p in tests_dir.rglob('test_*.py')}
        changed = True
        while changed:
            changed = False
            retired_test_modules = {Path(name).stem for name in direct_tests}
            for name, source in test_sources.items():
                if name not in direct_tests and deps(source) & retired_test_modules:
                    direct_tests[name] = {'dependent_on_retired_tests': sorted(deps(source) & retired_test_modules)}
                    changed = True
    return {'phase': PHASE, 'status': 'BLOCKED' if blocked else 'READY',
            'remaining_old_modules': old_present, 'blocking_production_refs': blocked,
            'legacy_tests_to_archive': direct_tests, 'legacy_scripts_to_archive': archival_scripts,
            'facade_api_change': old_src != new_src,
            'new_facade_source': new_src, 'full_pytest_run': False}


def apply(root: Path = ROOT) -> dict:
    root = Path(root)
    report = plan(root)
    new_source = report.pop('new_facade_source')
    destination = root/'phase165_r27_r59_r1_audit.json'
    if report['status'] != 'READY':
        report.update({'deleted_files': [], 'archived_tests': [], 'archived_scripts': [], 'modified_files': []})
        destination.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
        return report
    removals = [root / (m+'.py') for m in report['remaining_old_modules']]
    archived_tests = [root / name for name in report['legacy_tests_to_archive']]
    archived_scripts = [root / name for name in report['legacy_scripts_to_archive']]
    facade = root / (FACADE+'.py')
    backup = root/'phase165_r27_r59_r1_retirement_backup.zip'
    items = removals + archived_tests + archived_scripts + ([facade] if report['facade_api_change'] else [])
    if backup.exists() and items:
        raise RuntimeError('Refusing overwrite of existing retirement backup')
    if not items:
        report.update({'status': 'ALREADY_RETIRED', 'deleted_files': [], 'archived_tests': [], 'modified_files': []})
    else:
        # Write all original bytes and verify backup before destructive changes.
        with zipfile.ZipFile(backup, 'x', compression=zipfile.ZIP_DEFLATED) as z:
            for path in items:
                z.write(path, path.relative_to(root).as_posix())
        with zipfile.ZipFile(backup) as z:
            if set(z.namelist()) != {p.relative_to(root).as_posix() for p in items}:
                raise RuntimeError('Backup verification failure')
        if report['facade_api_change']:
            facade.write_text(new_source, encoding='utf-8')
        for path in removals + archived_tests + archived_scripts:
            path.unlink()
        report.update({'status': 'CHANGED', 'backup': backup.name,
                       'deleted_files': [p.relative_to(root).as_posix() for p in removals],
                       'archived_tests': [p.relative_to(root).as_posix() for p in archived_tests],
                       'archived_scripts': [p.relative_to(root).as_posix() for p in archived_scripts],
                       'modified_files': [facade.name] if report['facade_api_change'] else []})
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
