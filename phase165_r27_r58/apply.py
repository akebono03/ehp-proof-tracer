from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

PHASE = '165 R27-R58'
OLD_IMPORTS = {'toda_calculation_facade': {'build_toda_report'}, 'toda_calculation_result': {'TodaCalculationStatus'}}
NEW_FUNCTION = '''def _run_group_command(
    repository: ProofRepository,
    n: int,
    k: int,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    from toda_typed_group_facade import build_standard_toda_partial_result
    from phase165_r52_partial_proof import render_partial_proof_markdown

    try:
        result = build_standard_toda_partial_result(n=n, k=k)
    except (TypeError, ValueError) as error:
        print(f"error: {error}", file=stderr)
        return 2

    _write_markdown(stdout, render_partial_proof_markdown(result))
    return 0
'''


def _replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    found = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(found) != 1 or not isinstance(found[0], ast.FunctionDef):
        raise RuntimeError(f'expected exactly one function: {name}')
    node = found[0]
    args = [arg.arg for arg in node.args.args]
    if args != ['repository', 'n', 'k', 'stdout', 'stderr']:
        raise RuntimeError(f'unknown signature for {name}: {args}')
    lines = source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1]) + replacement + ''.join(lines[node.end_lineno:])


def _remove_unused_legacy_imports(source: str) -> str:
    tree = ast.parse(source)
    load_names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    edits = []
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.module not in OLD_IMPORTS:
            continue
        if any(alias.name not in OLD_IMPORTS[node.module] for alias in node.names):
            continue
        if any((alias.asname or alias.name) in load_names for alias in node.names):
            continue
        edits.append((node.lineno, node.end_lineno))
    lines = source.splitlines(keepends=True)
    for start, end in sorted(edits, reverse=True):
        del lines[start-1:end]
    return ''.join(lines)


def transform(source: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    fn = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_run_group_command']
    if len(fn) != 1:
        raise RuntimeError('unknown CLI group command')
    group_source = ast.get_source_segment(source, fn[0]) or ''
    if 'build_standard_toda_partial_result' in group_source and 'render_partial_proof_markdown' in group_source and 'build_toda_report(' not in group_source:
        updated = _remove_unused_legacy_imports(source)
    else:
        if 'build_toda_report(' not in group_source:
            raise RuntimeError('unknown existing group route; refusing overwrite')
        updated = _replace_function(source, '_run_group_command', NEW_FUNCTION)
        updated = _remove_unused_legacy_imports(updated)
    ast.parse(updated)
    return updated, updated != source


def audit(base: Path) -> dict:
    examined = {}
    for filename in ('cli.py', 'toda_calculation.py', 'toda_calculation_report.py', 'toda_calculation_facade.py'):
        p = base / filename
        if not p.exists():
            continue
        tree = ast.parse(p.read_text(encoding='utf-8-sig'))
        imported = sorted({n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module and (n.module.startswith('repository_') or n.module in {'toda_calculation', 'toda_calculation_report', 'toda_calculation_facade'})})
        examined[filename] = imported
    return examined


def apply(base: Path) -> dict:
    required = ('cli.py', 'toda_typed_group_facade.py', 'phase165_r52_partial_proof.py')
    missing = [x for x in required if not (base/x).is_file()]
    if missing:
        raise RuntimeError(f'missing required project files: {missing}')
    target = base/'cli.py'
    original = target.read_text(encoding='utf-8-sig')
    updated, changed = transform(original)
    if changed:
        backup = base/'phase165_r27_r58_backup'/'cli.py'
        backup.parent.mkdir(parents=True, exist_ok=True)
        if backup.exists() and backup.read_text(encoding='utf-8-sig') != original:
            raise RuntimeError('backup conflict; no files changed')
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_text(updated, encoding='utf-8')
    result = {'phase': PHASE, 'status': 'CHANGED' if changed else 'ALREADY_INSTALLED', 'modified_files': ['cli.py'] if changed else [], 'cli_group_uses_typed_partial_search': True, 'legacy_group_calculation_removed': False, 'remaining_legacy_repository_modules': sorted(p.stem for p in base.glob('repository_*.py')), 'audit_imports': audit(base), 'full_pytest_run': False}
    (base/'phase165_r27_r58_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(apply(Path(__file__).resolve().parent.parent), ensure_ascii=False, indent=2))
