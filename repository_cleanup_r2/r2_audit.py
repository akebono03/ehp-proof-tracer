"""Repository Cleanup R2: conservative read-only evidence audit.

No files are deleted, renamed, or changed outside its dedicated output folder.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
from collections import Counter

PROTECTED_NAMES = {
    'unified_statement_registry.py', 'phase163_source_archive_registry.py',
    'phase163_source_archive_catalog.json', 'proof_records.md',
    'development_log.md', 'design.md', 'roadmap.md',
}
CACHE_DIRS = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}
EVIDENCE_WORDS = ('manifest', 'source_catalog', 'audit', 'proof', 'record', 'evidence', 'registry')


def cache_candidate(path: str) -> bool:
    parts = path.replace('\\', '/').split('/')
    return any(p in CACHE_DIRS for p in parts[:-1]) or parts[-1].endswith(('.pyc', '.pyo'))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git_tracked(root: Path):
    try:
        p = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=40, check=False)
        if p.returncode != 0:
            return None, 'git ls-files failed: ' + p.stderr.decode('utf-8', 'replace')[:300]
        return {s.decode('utf-8', 'replace').replace('\\', '/')
                for s in p.stdout.split(b'\0') if s}, 'git ls-files succeeded'
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, type(e).__name__ + ': ' + str(e)


def evaluate(path: str, tracked: bool | None) -> tuple[str, str]:
    name = Path(path).name
    if cache_candidate(path):
        if tracked is None:
            return 'HOLD_GIT_UNKNOWN', 'Cache-shaped, but Git tracking could not be checked.'
        if tracked:
            return 'HOLD_TRACKED_CACHE', 'Cache-shaped but tracked in Git.'
        return 'CACHE_DELETE_CANDIDATE', 'Regenerable untracked cache; not deleted in R2.'
    if name in PROTECTED_NAMES or (name.endswith('.json') and any(x in name.lower() for x in EVIDENCE_WORDS)):
        return 'PRESERVE', 'Core file or possibly indispensable provenance evidence.'
    if name.lower().endswith(('.bak', '.backup', '.old', '.orig')):
        return 'REVIEW_BACKUP', 'Check content identity, references, and source history first.'
    return 'HOLD', 'No safe deletion decision without usage and provenance inspection.'


def write_csv(path: Path, rows: list[dict]):
    fields = ['Path', 'R1Category', 'R2Decision', 'Reason', 'Tracked', 'Exists',
              'Bytes', 'SHA256', 'IdenticalTo']
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path, r1: Path, output: Path) -> dict:
    root = root.resolve()
    output = output.resolve()
    if not (root / 'unified_statement_registry.py').is_file():
        raise ValueError('Project root is missing unified_statement_registry.py')
    if output == root or root not in output.parents:
        raise ValueError('Output must be a dedicated child folder under project root')
    if not r1.is_file():
        raise FileNotFoundError(str(r1))
    tracked, git_message = git_tracked(root)
    with r1.open(newline='', encoding='utf-8-sig') as f:
        originals = list(csv.DictReader(f))
    if not originals or any(not x.get('Path') or not x.get('Category') for x in originals):
        raise ValueError('Invalid R1 inventory')
    rows = []
    backups = []
    for item in originals:
        rel = item['Path'].replace('\\', '/')
        target = (root / rel).resolve()
        if root not in target.parents or target == root:
            raise ValueError('Unsafe inventory path: ' + rel)
        exists = target.is_file()
        is_tracked = None if tracked is None else rel in tracked
        decision, reason = evaluate(rel, is_tracked)
        if not exists:
            decision, reason = 'MISSING', 'Present in R1 but no longer present on disk.'
        row = {'Path': rel, 'R1Category': item['Category'], 'R2Decision': decision,
               'Reason': reason, 'Tracked': 'UNKNOWN' if is_tracked is None else str(is_tracked),
               'Exists': str(exists), 'Bytes': item.get('Bytes', ''), 'SHA256': '', 'IdenticalTo': ''}
        if exists and decision == 'REVIEW_BACKUP':
            row['SHA256'] = digest(target)
            backups.append(row)
        rows.append(row)
    # Exact-content comparison for backup files only. Identical does not imply safe deletion.
    hashes = {}
    for row in backups:
        hashes.setdefault(row['SHA256'], []).append(row['Path'])
    for row in backups:
        others = [p for p in hashes[row['SHA256']] if p != row['Path']]
        # Compare with a plausible current file when backup is at project root.
        current_name = row['Path'].split('/')[-1].split('.phase')[0]
        if '/' not in row['Path'] and current_name.endswith('.py'):
            candidate = root / current_name
            if candidate.is_file() and digest(candidate) == row['SHA256']:
                others.append(current_name)
        row['IdenticalTo'] = '; '.join(sorted(set(others))[:12])
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'r2_decisions.csv', rows)
    write_csv(output / 'r2_cache_candidates.csv', [r for r in rows if r['R2Decision'] == 'CACHE_DELETE_CANDIDATE'])
    write_csv(output / 'r2_backup_review.csv', backups)
    decisions = Counter(x['R2Decision'] for x in rows)
    summary = {'phase': 'Repository Cleanup R2', 'mode': 'READ_ONLY',
               'r1_files': len(originals), 'git_status': git_message,
               'decisions': dict(sorted(decisions.items())),
               'backup_exact_duplicate_groups': sum(len(v) > 1 for v in hashes.values()),
               'production_files_modified': False, 'deletions': 0,
               'pytest_run': False,
               'limitations': [
                 'R2 does not prove all runtime, dynamic import, test, or script dependencies.',
                 'Backup identity alone is never a deletion authorization.',
                 'Phase source catalogs, manifests, audit JSON and proof evidence remain protected.',
                 'Git tracking unknown means no cache file is approved for deletion.',
               ]}
    (output / 'r2_summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Repository Cleanup R2 - Read-only review', '',
             'Files: ' + str(len(originals)), 'Git: ' + git_message, '',
             '## Decisions'] + ['- ' + k + ': ' + str(v) for k, v in sorted(decisions.items())]
    lines += ['', '## Important',
              '- No files deleted or moved; only report files written.',
              '- CACHE_DELETE_CANDIDATE requires a separate R3 confirmation and tracked=false.',
              '- REVIEW_BACKUP requires manual/provenance confirmation, even if byte-identical.',
              '- Core code, tests, mathematical records and Phase 163 archives are retained.',
              '- Full pytest not run; no pytest executed in R2.',
              '- This focused pass is not a complete dependency graph.',
              '', '## Outputs', '- r2_decisions.csv', '- r2_cache_candidates.csv',
              '- r2_backup_review.csv', '- r2_summary.json']
    (output / 'r2_report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--r1', type=Path)
    args = parser.parse_args()
    root = args.project.resolve()
    r1 = args.r1 or root / 'repository_cleanup_r1_output' / 'inventory.csv'
    summary = run(root, r1, root / 'repository_cleanup_r2_output')
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    print('Report:', root / 'repository_cleanup_r2_output' / 'r2_report.md')


if __name__ == '__main__':
    main()
