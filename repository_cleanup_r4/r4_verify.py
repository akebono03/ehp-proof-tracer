"""Repository Cleanup R4: read-only final audit and targeted tests only."""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

REQUIRED = (
    'unified_statement_registry.py',
    'phase163_source_archive_registry.py',
    'phase163_source_archive_catalog.json',
    'phase163_r4_r95_phase_closure/r95_phase_closure.py',
    'phase163_r4_r95_phase_closure/tests/test_r95_phase_closure.py',
    'phase163_r4_r94_registry_finalization/tests/test_r94_registry_finalization.py',
    'tests/test_phase163_r2_unified_registry.py',
    'tests/test_phase163_r4_registry_bridge.py',
    'phase163_r4_r94_output/manifest.json',
    'phase163_r4_r91_output/source_catalog.json',
    'phase163_r4_r92_output/audit.json',
    'sources/toda',
    'repository_cleanup_r3_output/r3_summary.json',
    'repository_cleanup_r3_output/r3_deleted.csv',
)
TESTS = (
    'phase163_r4_r95_phase_closure/tests/test_r95_phase_closure.py',
    'phase163_r4_r94_registry_finalization/tests/test_r94_registry_finalization.py',
    'tests/test_phase163_r2_unified_registry.py',
    'tests/test_phase163_r4_registry_bridge.py',
    'repository_cleanup_r4/test_r4_verify.py',
)


def git_snapshot(project: Path) -> tuple[str, ...]:
    """Capture tracked working-tree changes including staged changes."""
    p = subprocess.run(
        ['git', 'status', '--porcelain=v1', '--untracked-files=no'],
        cwd=project, capture_output=True, text=True, encoding='utf-8', errors='replace',
        check=True,
    )
    return tuple(sorted(p.stdout.splitlines()))


def validate_r3(summary: dict, rows: list[dict], project: Path) -> dict:
    """Verify R3 counts and that all recorded deleted cache files remain absent."""
    count = int(summary.get('deleted_files', -1))
    size = int(summary.get('deleted_bytes', -1))
    valid = (
        summary.get('phase') == 'Repository Cleanup R3'
        and summary.get('mode') == 'APPLY_CACHE_ONLY'
        and count == 3276
        and count == len(rows)
        and size == sum(int(row['Bytes']) for row in rows)
        and summary.get('deletion_failures') == 0
        and summary.get('tracked_status_unchanged') is True
        and summary.get('tracked_files_modified_by_cleanup') is False
        and summary.get('backups_deleted') == 0
    )
    missing = []
    unsafe = []
    seen = set()
    root = project.resolve()
    for row in rows:
        name = row.get('Path', '')
        normalized = name.replace('\\', '/')
        parts = Path(normalized).parts
        if (not normalized or normalized.startswith('/') or ':' in normalized
                or '..' in parts or normalized in seen
                or not (('/__pycache__/' in '/' + normalized)
                        or ('/.pytest_cache/' in '/' + normalized)
                        or normalized.endswith(('.pyc', '.pyo')))):
            unsafe.append(normalized)
            continue
        seen.add(normalized)
        location = root.joinpath(*parts)
        if location.is_symlink() or location.exists():
            missing.append(normalized)
    return {'r3_log_consistent': valid and not unsafe,
            'cache_reappeared_count': len(missing),
            'cache_reappeared_examples': missing[:15],
            'invalid_log_entries': unsafe[:15],
            'logged_deleted_files': len(rows), 'logged_deleted_bytes': size}


def execute(project: Path, output: Path) -> int:
    if not (project / 'unified_statement_registry.py').is_file():
        raise ValueError('Not an EHP Proof Tracer project root')
    output.mkdir(parents=True, exist_ok=True)
    missing = [p for p in REQUIRED if not (project / p).exists()]
    git_before = git_snapshot(project)
    details = {}
    if not missing:
        summary = json.loads((project / 'repository_cleanup_r3_output/r3_summary.json').read_text(encoding='utf-8-sig'))
        with (project / 'repository_cleanup_r3_output/r3_deleted.csv').open(encoding='utf-8-sig', newline='') as stream:
            records = list(csv.DictReader(stream))
        details = validate_r3(summary, records, project)

    passed_preflight = not missing and details['r3_log_consistent'] and details['cache_reappeared_count'] == 0
    returncode = None
    log = 'Not run: preflight failed.\n'
    if passed_preflight:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(project), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
        command = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *TESTS]
        process = subprocess.run(command, cwd=project, env=env, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 encoding='utf-8', errors='replace')
        returncode = process.returncode
        log = process.stdout
    (output / 'r4_targeted_pytest.log').write_text(log, encoding='utf-8')
    git_after = git_snapshot(project)
    result = {
        'phase': 'Repository Cleanup R4',
        'mode': 'FINAL_CHECK_TARGETED_ONLY',
        'required_paths_present': not missing,
        'missing_required_paths': missing,
        **details,
        'git_tracked_status_unchanged': git_before == git_after,
        'tracked_changes_before': list(git_before),
        'tracked_changes_after': list(git_after),
        'targeted_pytest_returncode': returncode,
        'targeted_test_paths': list(TESTS) if passed_preflight else [],
        'full_pytest_run': False,
        'files_deleted': 0,
        'phase164_ready': passed_preflight and returncode == 0 and git_before == git_after,
    }
    (output / 'r4_summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Repository Cleanup R4 - Final check', '',
             f"- Status: {'PASS' if result['phase164_ready'] else 'FAIL / REVIEW'}",
             f"- Required files present: {result['required_paths_present']}",
             f"- R3 log consistent: {details.get('r3_log_consistent', False)}",
             f"- Cache reappeared: {details.get('cache_reappeared_count', 'unknown')}",
             f"- Tracked Git status unchanged: {result['git_tracked_status_unchanged']}",
             f"- Targeted pytest exit code: {returncode}",
             '- Full pytest: NOT RUN', '- Deletions: NONE', '',
             '## Test output', 'See r4_targeted_pytest.log.', '',
             '## Scope', 'No changes to proof registry, source evidence, tests, or prior Phase files.',
             'This confirms the cache-only cleanup; historical artifact consolidation is out of scope.']
    (output / 'r4_report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('tracked_changes_before', 'tracked_changes_after', 'targeted_test_paths')}, ensure_ascii=False, indent=2))
    print('Report:', output / 'r4_report.md')
    return 0 if result['phase164_ready'] else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    raise SystemExit(execute(project, project / 'repository_cleanup_r4_output'))


if __name__ == '__main__':
    main()
