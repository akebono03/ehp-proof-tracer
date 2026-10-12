"""Repository Cleanup R3: allowlisted, tracked-safe cache deletion only."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
from collections import Counter

CACHE_DIRS = frozenset({'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'})
FIELDS = ('Path', 'R1Category', 'R2Decision', 'Reason', 'Tracked', 'Exists', 'Bytes', 'SHA256', 'IdenticalTo')


def is_cache_path(relative: str) -> bool:
    parts = relative.split('/')
    return (len(parts) > 1 and any(part in CACHE_DIRS for part in parts[:-1])) or parts[-1].endswith(('.pyc', '.pyo'))


def tracked_paths(root: Path) -> set[str]:
    completed = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'], capture_output=True, timeout=60, check=False)
    if completed.returncode:
        raise RuntimeError('git ls-files failed: ' + completed.stderr.decode('utf-8', 'replace')[:300])
    return {item.decode('utf-8', 'surrogateescape').replace('\\', '/') for item in completed.stdout.split(b'\0') if item}


def tracked_status(root: Path) -> bytes:
    result = subprocess.run(['git', '-C', str(root), 'status', '--porcelain=v1', '-z', '-uno'], capture_output=True, timeout=60, check=False)
    if result.returncode:
        raise RuntimeError('git status failed')
    return result.stdout


def load_candidates(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not set(FIELDS).issubset(reader.fieldnames or ()):
            raise ValueError('R2 candidate CSV fields invalid')
        entries = list(reader)
    if not entries or len({x['Path'] for x in entries}) != len(entries):
        raise ValueError('R2 candidate CSV empty or duplicate paths')
    return entries


def validate(root: Path, row: dict[str, str], tracked: set[str], excluded: set[str]) -> tuple[Path | None, str]:
    rel = row['Path']
    if not isinstance(rel, str) or not rel or '\\' in rel or rel.startswith('/') or ':' in rel or any(x in ('', '.', '..') for x in rel.split('/')):
        return None, 'INVALID_PATH'
    if not is_cache_path(rel) or any(part == '.git' for part in rel.split('/')):
        return None, 'NOT_CACHE'
    if row['R1Category'] != 'CACHE_CANDIDATE' or row['R2Decision'] != 'CACHE_DELETE_CANDIDATE' or row['Tracked'] != 'False' or row['Exists'] != 'True':
        return None, 'NOT_R2_APPROVED'
    if rel in tracked:
        return None, 'NOW_GIT_TRACKED'
    target = root.joinpath(*rel.split('/'))
    if any(rel == prefix or rel.startswith(prefix + '/') for prefix in excluded):
        return None, 'OUTPUT_PATH'
    if any(p.is_symlink() for p in (target, *list(target.parents)[:-1]) if p == target or root in p.parents):
        return None, 'SYMLINK'
    resolved = target.resolve()
    if root not in resolved.parents:
        return None, 'ESCAPES_ROOT'
    if not target.is_file():
        return None, 'MISSING'
    try:
        expected = int(row['Bytes'])
    except (ValueError, TypeError):
        return None, 'BAD_SIZE'
    if expected != target.stat().st_size:
        return None, 'SIZE_CHANGED'
    return target, 'APPROVED'


def run(root: Path, candidate_csv: Path, output: Path, apply: bool = False) -> dict:
    root = root.resolve()
    candidate_csv = candidate_csv.resolve()
    output = output.resolve()
    if not (root / 'unified_statement_registry.py').is_file():
        raise ValueError('Not an EHP Proof Tracer project root')
    if root not in output.parents or output == root:
        raise ValueError('Output directory must be inside project root')
    if root not in candidate_csv.parents:
        raise ValueError('Candidate CSV must be inside project root')
    rows = load_candidates(candidate_csv)
    tracked = tracked_paths(root)
    before = tracked_status(root)
    excluded = {output.relative_to(root).as_posix(), candidate_csv.parent.relative_to(root).as_posix(), 'repository_cleanup_r3'}
    approvals = []
    blockers = []
    for row in rows:
        path, reason = validate(root, row, tracked, excluded)
        if reason == 'APPROVED':
            approvals.append((row, path))
        else:
            blockers.append({'Path': row['Path'], 'Reason': reason})
    # A stale/modified inventory is not allowed to cause a partial delete.
    fatal = [x for x in blockers if x['Reason'] != 'MISSING']
    if apply and fatal:
        raise RuntimeError(f'Preflight blocked: {len(fatal)} non-missing candidate(s); nothing deleted')
    deleted = []
    failures = []
    if apply:
        for row, target in approvals:
            # Re-verify path, file type and size immediately before unlinking.
            current, reason = validate(root, row, tracked, excluded)
            if reason != 'APPROVED' or current != target:
                failures.append({'Path': row['Path'], 'Reason': reason})
                break
            try:
                target.unlink()
                deleted.append({'Path': row['Path'], 'Bytes': int(row['Bytes'])})
            except OSError as exc:
                failures.append({'Path': row['Path'], 'Reason': type(exc).__name__})
                break
    after = tracked_status(root)
    output.mkdir(parents=True, exist_ok=True)
    summary = {
        'phase': 'Repository Cleanup R3',
        'mode': 'APPLY_CACHE_ONLY' if apply else 'DRY_RUN',
        'r2_candidates': len(rows),
        'approved_at_preflight': len(approvals),
        'missing_at_preflight': sum(x['Reason'] == 'MISSING' for x in blockers),
        'blocked_at_preflight': len(fatal),
        'deleted_files': len(deleted),
        'deleted_bytes': sum(x['Bytes'] for x in deleted),
        'deletion_failures': len(failures),
        'tracked_status_unchanged': before == after,
        'tracked_files_modified_by_cleanup': False if before == after else 'UNVERIFIED',
        'backups_deleted': 0,
        'pytest_run': False,
    }
    (output / 'r3_summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    with (output / 'r3_deleted.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['Path', 'Bytes'])
        writer.writeheader()
        writer.writerows(deleted)
    with (output / 'r3_skipped.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['Path', 'Reason'])
        writer.writeheader()
        writer.writerows(blockers + failures)
    lines = ['# Repository Cleanup R3', '', f"- Mode: {summary['mode']}", f"- R2 candidates: {len(rows)}", f"- Deleted: {len(deleted)}", f"- Freed bytes: {summary['deleted_bytes']}", f"- Skipped: {len(blockers) + len(failures)}", f"- Git tracked status unchanged: {before == after}", '- Source, tests, JSON, documentation, backups: not targeted', '- Full pytest: not run', '', 'Only paths explicitly approved by R2 were eligible.']
    (output / 'r3_report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if failures or before != after:
        raise RuntimeError('R3 encountered a deletion failure or tracked Git status change; see report')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--r2', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = args.project.resolve()
    r2 = args.r2 or (root / 'repository_cleanup_r2_output' / 'r2_cache_candidates.csv')
    result = run(root, r2, root / 'repository_cleanup_r3_output', apply=args.apply)
    print(json.dumps(result, indent=2))
    print('Report:', root / 'repository_cleanup_r3_output' / 'r3_report.md')


if __name__ == '__main__':
    main()
