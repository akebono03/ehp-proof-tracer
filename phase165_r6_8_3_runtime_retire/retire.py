"""Phase 165 R6-8(3): retire legacy cluster by production reachability.

This does not assert anything about mathematical proof correctness or pytest collection.
"""
from __future__ import annotations
import argparse
import ast
import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOTS = ('web_app.py', 'phase165_r55_nk_only_goal.py', 'phase165_r52_r9_shared_math.py')
CANDIDATES = (
    'probes/probe_phase53_capabilities.py',
    'probes/probe_phase54_capabilities.py',
    'probes/probe_phase55_capabilities.py',
    'probes/probe_phase57_capabilities.py',
    'phase162_ehp_leaf_inputs.py',
    'phase162_pi5_3_web_replay.py',
    'tests/test_phase59_n3_ehp_chain.py',
    'tests/test_phase55_prop51_phase52_phase54_dependency.py',
)
EXCLUDE = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', 'node_modules'}


def module_name(path: str) -> str:
    return path[:-3].replace('/', '.') if path.endswith('.py') else path


def module_files(root: Path) -> dict[str, Path]:
    files = {}
    for path in sorted(root.glob('*.py')):
        files[path.stem] = path
    for base in ('probes', 'tests'):
        folder = root / base
        if folder.is_dir():
            for path in sorted(folder.glob('*.py')):
                files[module_name(path.relative_to(root).as_posix())] = path
    # Additional production packages are admitted ONLY if imported by current
    # runtime code, avoiding the thousands of archived phase-specific packages.
    return files


def inspect_imports(path: Path, module: str):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    dependencies = set()
    dynamics = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            dependencies.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = node.module or ''
            if node.level and '.' in module:
                package = module.split('.')[:-1]
                package = package[:max(0, len(package) - node.level + 1)]
                prefix = '.'.join(package + ([prefix] if prefix else []))
            if prefix:
                dependencies.add(prefix)
                dependencies.update(prefix + '.' + alias.name for alias in node.names)
        elif isinstance(node, ast.Call):
            func = node.func
            dynamic = (isinstance(func, ast.Name) and func.id == '__import__') or (
                isinstance(func, ast.Attribute) and func.attr == 'import_module'
            )
            if dynamic:
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    dependencies.add(node.args[0].value)
                else:
                    dynamics.append(node.lineno)
    return dependencies, dynamics


def plan(root: Path) -> dict:
    files = module_files(root)
    missing_roots = [p for p in ROOTS if not (root / p).is_file()]
    absent = [p for p in CANDIDATES if not (root / p).is_file()]
    to_visit = deque(module_name(p) for p in ROOTS)
    visited = set()
    parent = {}
    parse_errors = []
    dynamic_calls = []
    while to_visit:
        name = to_visit.popleft()
        if name in visited:
            continue
        visited.add(name)
        path = files.get(name)
        if path is None:
            # Check imported production package paths lazily.
            candidate = root.joinpath(*name.split('.')).with_suffix('.py')
            if candidate.is_file() and not any(part in EXCLUDE for part in candidate.relative_to(root).parts):
                path = candidate
            else:
                continue
        try:
            deps, dynamics = inspect_imports(path, name)
        except (SyntaxError, UnicodeError, OSError) as exc:
            parse_errors.append({'module': name, 'error': str(exc)})
            continue
        if dynamics:
            dynamic_calls.append({'module': name, 'lines': dynamics})
        for dep in sorted(deps):
            if dep not in visited:
                parent.setdefault(dep, name)
                to_visit.append(dep)
    protected = []
    removable = []
    for rel in CANDIDATES:
        if rel in absent:
            continue
        mod = module_name(rel)
        (protected if mod in visited else removable).append(rel)
    return {
        'phase': '165 R6-8(3)', 'criterion': 'production_root_reachability',
        'roots': list(ROOTS), 'visited_module_count': len(visited),
        'protected': protected, 'retirable': removable, 'missing': absent,
        'missing_roots': missing_roots, 'parse_errors': parse_errors,
        'nonliteral_dynamic_imports': dynamic_calls,
        'safe_to_apply': not (missing_roots or parse_errors or dynamic_calls),
        'mathematical_coverage_verified': False, 'pytest_collection_verified': False,
        'full_pytest_run': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    report = plan(root)
    report['action'] = 'preview'
    if args.apply and report['safe_to_apply'] and report['retirable']:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup = root / f'phase165_r6_8_3_runtime_backup_{stamp}.zip'
        with ZipFile(backup, 'w', ZIP_DEFLATED) as archive:
            for rel in report['retirable']:
                archive.write(root / rel, rel)
        with ZipFile(backup) as archive:
            for rel in report['retirable']:
                if archive.read(rel) != (root / rel).read_bytes():
                    raise RuntimeError(f'Backup verification failed: {rel}')
        for rel in report['retirable']:
            (root / rel).unlink()
        report['action'] = 'retired_production_unreachable_files'
        report['backup'] = str(backup)
    elif args.apply:
        report['action'] = 'blocked_or_empty'
    output = root / 'phase165_r6_8_3_runtime_retire_report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['safe_to_apply'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
