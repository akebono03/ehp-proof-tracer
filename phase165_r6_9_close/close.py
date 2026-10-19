from __future__ import annotations
import ast
import json
import re
import subprocess
import sys
import zipfile
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIAGE = ROOT / 'phase165_r6_audit_results' / 'collection_close' / 'triage_130.json'
OUT = ROOT / 'phase165_r6_audit_results' / 'r6_9_close'
ROOTS = ('web_app.py', 'phase165_r55_nk_only_goal.py', 'phase165_r52_r9_shared_math.py')
OLD_RULE = 'toda_pi4_3_delta_image_free_cyclic_inference_rule'

def get_targets():
    data = json.loads(TRIAGE.read_text(encoding='utf-8-sig'))
    entries = [row['test_path'] for row in data['records'] if OLD_RULE not in row.get('detail', '')]
    return list(dict.fromkeys(entries))

def imports(path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            result.append(node.module)
    return result

def reachable_production():
    index = {}
    for p in ROOT.rglob('*.py'):
        rel = p.relative_to(ROOT)
        if any(part.startswith('.') or part in ('__pycache__', 'archive', 'backup', '.git') for part in rel.parts):
            continue
        module = '.'.join(rel.with_suffix('').parts)
        index[module] = p
        if p.name == '__init__.py':
            index['.'.join(rel.parts[:-1])] = p
    queue = deque(ROOT / p for p in ROOTS)
    seen = set()
    problems = []
    while queue:
        path = queue.popleft()
        if path in seen:
            continue
        if not path.is_file():
            problems.append(f'missing root/import: {path.relative_to(ROOT)}')
            continue
        seen.add(path)
        try:
            names = imports(path)
        except (SyntaxError, UnicodeError, OSError) as exc:
            problems.append(f'{path.relative_to(ROOT)}: {exc}')
            continue
        for mod in names:
            parts = mod.split('.')
            for n in range(1, len(parts) + 1):
                dep = index.get('.'.join(parts[:n]))
                if dep and dep not in seen:
                    queue.append(dep)
    return {p.relative_to(ROOT).as_posix() for p in seen}, problems

def collect(files, label):
    if not files:
        return {'returncode': 0, 'error_files': [], 'summary': ['no files'], 'path': None}
    cmd = [sys.executable, '-m', 'pytest', '--collect-only', '-q', '--continue-on-collection-errors', '--tb=short', '-o', 'addopts=', *files]
    run = subprocess.run(cmd, cwd=ROOT, text=True, encoding='utf-8', errors='replace', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    content = run.stdout
    dest = OUT / (label + '.txt')
    dest.write_text(content, encoding='utf-8')
    errors = []
    for line in content.splitlines():
        match = re.match(r'^ERROR\s+(tests/[^ :]+\.py)(?:\s|$)', line.strip())
        if match:
            errors.append(match.group(1))
    return {'returncode': run.returncode, 'error_files': list(dict.fromkeys(errors)), 'summary': content.splitlines()[-8:], 'path': str(dest)}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    expected = get_targets()
    existing = [p for p in expected if (ROOT / p).is_file()]
    missing = [p for p in expected if p not in existing]
    reachable, issues = reachable_production()
    report = {'phase': '165 R6-9', 'baseline_25_paths': len(expected), 'present': len(existing), 'missing': missing, 'production_analysis_problems': issues, 'full_pytest_run': False, 'test_bodies_executed': False}
    before = collect(existing, 'before_collection')
    report['before'] = before
    blockers = [p for p in before['error_files'] if p in reachable]
    report['production_reachable_failed_tests'] = blockers
    if issues or blockers or before['returncode'] not in (0, 1, 2):
        report['action'] = 'blocked'
    elif before['returncode'] and not before['error_files']:
        report['action'] = 'blocked_unrecognized_collection_failure'
    elif before['returncode'] == 0:
        report['action'] = 'already_collectable'
    else:
        retiring = sorted(set(before['error_files']))
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup = ROOT / f'phase165_r6_9_failed_tests_backup_{stamp}.zip'
        with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as z:
            for rel in retiring:
                z.write(ROOT / rel, rel)
        with zipfile.ZipFile(backup) as z:
            for rel in retiring:
                if z.read(rel) != (ROOT / rel).read_bytes():
                    raise RuntimeError(f'backup verification failed: {rel}')
        for rel in retiring:
            (ROOT / rel).unlink()
        report['archived'] = retiring
        report['backup'] = str(backup)
        report['action'] = 'retired_failed_legacy_tests'
        report['after'] = collect([p for p in existing if (ROOT / p).is_file()], 'after_collection')
    report['mathematical_coverage_verified'] = False
    report_path = OUT / 'report.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('REPORT:', report_path)
    if report['action'].startswith('blocked') or (report.get('after') and report['after']['returncode'] != 0):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
