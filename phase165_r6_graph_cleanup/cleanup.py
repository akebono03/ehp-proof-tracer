"""Phase 165 R6: dependency-closed cleanup for legacy collection failures."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HEADER = re.compile(r'^\s*_+\s+ERROR collecting\s+(.*?)\s+_+\s*$', re.M)
PHASE = re.compile(r'^test_phase(\d+)(?:_|$)')
SUMMARY = re.compile(r'(\d+) errors? in [\d.]+s')
OLD = ('repository_inference', 'repository_element_', 'repository_generator_', 'repository_known_', 'toda_pi4_3_delta_image_free_cyclic_inference_rule', 'probes.probe_phase50_capabilities')

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def imported_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    result = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result

def get_errors(log: str) -> dict[str, str]:
    matches = list(HEADER.finditer(log))
    return {m.group(1).strip().replace('\\', '/'): log[m.end():matches[i+1].start() if i+1 < len(matches) else len(log)] for i, m in enumerate(matches)}

def build_plan(root: Path, log: str) -> dict:
    blocks = get_errors(log)
    summary_matches = SUMMARY.findall(log)
    reported = int(summary_matches[-1]) if summary_matches else None
    if reported is None or reported != len(blocks):
        raise ValueError(f'Collection count mismatch: {reported} vs {len(blocks)}; no deletion')
    paths = sorted((root/'tests').glob('test_*.py')) + sorted(root.glob('test_*.py'))
    modules = {}
    parse_errors = {}
    for p in paths:
        rel = p.relative_to(root).as_posix()
        try:
            modules[rel] = imported_names(p)
        except (SyntaxError, UnicodeError, ValueError) as exc:
            parse_errors[rel] = str(exc)
    if parse_errors:
        raise ValueError('Unparseable tests: ' + json.dumps(parse_errors, ensure_ascii=False))
    reverse = defaultdict(set)
    for rel, imports in modules.items():
        for name in imports:
            reverse[name].add(rel)
    failed = set(blocks)
    candidates = set()
    rows = {}
    for rel, chunk in sorted(blocks.items()):
        p = root/rel
        match = PHASE.match(p.stem)
        legacy_error = any(marker in chunk for marker in OLD)
        eligible = (p.is_file() and p.parent == root/'tests' and match is not None and int(match.group(1)) <= 129 and legacy_error)
        rows[rel] = {'path': rel, 'candidate': eligible, 'legacy_error': legacy_error, 'reason': None if eligible else 'PROTECTED_OR_UNVERIFIED'}
        if eligible:
            candidates.add(rel)
    # Fixed-point: keep every candidate imported by a surviving test; trim its dependencies accordingly.
    while True:
        remove = set()
        for rel in candidates:
            stem = Path(rel).stem
            callers = (reverse.get(stem, set()) | reverse.get('tests.' + stem, set())) - {rel}
            if any(caller not in candidates for caller in callers):
                remove.add(rel)
        if not remove:
            break
        candidates -= remove
    for rel in rows:
        if rel in candidates:
            rows[rel]['decision'] = 'REMOVE'
            rows[rel]['sha256'] = sha(root/rel)
        else:
            rows[rel]['decision'] = 'KEEP'
            if rows[rel]['candidate']:
                rows[rel]['reason'] = 'IMPORTED_BY_SURVIVING_TEST_TRANSITIVELY'
    return {'reported_errors': reported, 'error_files': len(blocks), 'candidate_count': sum(r['candidate'] for r in rows.values()), 'remove_count': len(candidates), 'retained_count': len(rows)-len(candidates), 'decisions': list(rows.values())}

def execute(root: Path, plan: dict, backup: Path) -> None:
    selected = [r for r in plan['decisions'] if r['decision'] == 'REMOVE']
    for r in selected:
        source = root/r['path']
        if sha(source) != r['sha256'] or (backup/r['path']).exists():
            raise RuntimeError('Changed source or backup collision: ' + r['path'])
    for r in selected:
        src = root/r['path']
        dst = backup/r['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if sha(dst) != r['sha256']:
            raise RuntimeError('Backup verification failed: ' + r['path'])
    for r in selected:
        (root/r['path']).unlink()
        r['result'] = 'BACKED_UP_AND_REMOVED'

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    logpath = root/'phase165_r6_audit_results'/'recollection'/'collection.log'
    log = logpath.read_text(encoding='utf-8', errors='replace')
    plan = build_plan(root, log)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    session = root/'phase165_r6_audit_results'/'graph_cleanup'/stamp
    session.mkdir(parents=True, exist_ok=False)
    plan['mode'] = 'APPLY' if args.apply else 'DRY_RUN'
    plan['baseline_log'] = str(logpath)
    if args.apply:
        execute(root, plan, session/'backup')
    report = session/'report.json'
    report.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Errors in baseline: {plan["reported_errors"]}; eligible: {plan["candidate_count"]}; removed: {plan["remove_count"] if args.apply else 0}; retained: {plan["retained_count"]}')
    print('Report:', report)
    if args.apply:
        print('Recollecting only; test bodies will not run.')
        command = [sys.executable, '-m', 'pytest', '--collect-only', '-q', '--continue-on-collection-errors', 'tests']
        command.extend(str(p.name) for p in sorted(root.glob('test_*.py')))
        with (session/'collection.log').open('w', encoding='utf-8', errors='replace') as stream:
            run = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=False)
        after_log = (session/'collection.log').read_text(encoding='utf-8', errors='replace')
        try:
            after = get_errors(after_log)
            count = int(SUMMARY.findall(after_log)[-1]) if SUMMARY.findall(after_log) else 0
            plan['after'] = {'returncode': run.returncode, 'error_files': len(after), 'summary_errors': count, 'consistent': count == len(after)}
        except Exception as exc:
            plan['after'] = {'returncode': run.returncode, 'parser_error': str(exc)}
        report.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding='utf-8')
        print('After collection:', plan['after'])
        print('After log:', session/'collection.log')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
