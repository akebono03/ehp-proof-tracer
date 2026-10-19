"""Archive the historical 105-path collection-error cohort without modifying production code."""
from __future__ import annotations
import argparse
import ast
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOTS = ('web_app.py', 'phase165_r55_nk_only_goal.py', 'phase165_r52_r9_shared_math.py')
BASELINE = 'phase165_r6_audit_results/collection_close/r6_8_dependency_chains.json'

def imports(path: Path, module: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = node.module or ''
            if node.level:
                package = module.split('.')[:-1]
                package = package[:max(0, len(package) - node.level + 1)]
                prefix = '.'.join(package + ([prefix] if prefix else []))
            if prefix:
                found.add(prefix)
                found.update(prefix + '.' + a.name for a in node.names)
        elif isinstance(node, ast.Call):
            f = node.func
            if (isinstance(f, ast.Name) and f.id == '__import__') or (isinstance(f, ast.Attribute) and f.attr == 'import_module'):
                if not node.args or not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, str):
                    raise RuntimeError(f'Unresolved dynamic import: {path}:{node.lineno}')
                found.add(node.args[0].value)
    return found

def runtime_reachable(root: Path) -> set[str]:
    work = deque(p[:-3] for p in ROOTS)
    found = set()
    while work:
        mod = work.popleft()
        if mod in found:
            continue
        found.add(mod)
        path = root.joinpath(*mod.split('.')).with_suffix('.py')
        if not path.is_file():
            continue
        for dep in imports(path, mod):
            if dep not in found:
                work.append(dep)
    return found

def cohort(root: Path) -> list[str]:
    data = json.loads((root / BASELINE).read_text(encoding='utf-8'))
    rows = data['test_dependencies']
    if len(rows) != 105:
        raise RuntimeError(f'Unexpected baseline size: {len(rows)}; expected 105')
    paths = sorted({r['test_path'] for r in rows})
    if len(paths) != 105 or any(not p.startswith('tests/test_') or not p.endswith('.py') or '..' in p for p in paths):
        raise RuntimeError('Unrecognized baseline path list')
    return paths

def execute(root: Path, apply: bool) -> dict:
    paths = cohort(root)
    present = [p for p in paths if (root / p).is_file()]
    missing = [p for p in paths if p not in present]
    reachable = runtime_reachable(root)
    protected = [p for p in present if p[:-3].replace('/', '.') in reachable]
    # Guard imports of target test modules from all files in active production scope.
    # The reachability set already covers Python imports from the declared runtime roots.
    report = {'phase':'165 R6-8(4)', 'purpose':'retire_old_collection_tests',
              'baseline_count':len(paths), 'present':len(present), 'missing':missing,
              'production_reachable_test_paths':protected,
              'files_to_archive':present, 'mathematical_coverage_verified':False,
              'remaining_collection_verified':False,'full_pytest_run':False,'action':'preview'}
    if apply and protected:
        report['action'] = 'blocked_production_dependency'
    elif apply and present:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        dest = root / f'phase165_r6_8_4_legacy_tests_backup_{stamp}.zip'
        with ZipFile(dest, 'w', ZIP_DEFLATED) as z:
            for p in present:
                z.write(root / p, p)
        with ZipFile(dest) as z:
            for p in present:
                if z.read(p) != (root / p).read_bytes():
                    raise RuntimeError(f'Backup mismatch: {p}; NOTHING removed')
        for p in present:
            (root / p).unlink()
        report['action'] = 'archived_legacy_cohort'
        report['backup'] = str(dest)
        report['archived'] = len(present)
    elif apply:
        report['action'] = 'already_archived'
    (root / 'phase165_r6_8_4_legacy_test_retirement_report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        report = execute(args.root.resolve(), args.apply)
    except (OSError, ValueError, RuntimeError, SyntaxError) as e:
        print(json.dumps({'action':'blocked','error':str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report['action'] == 'blocked_production_dependency' else 0

if __name__ == '__main__':
    raise SystemExit(main())
