"""Phase 165: run bounded, current-target tests and report three goal states."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase165_r6_audit_results' / 'final_targeted'
OUT.mkdir(parents=True, exist_ok=True)


def execute(args: list[str], timeout: int, filename: str) -> dict:
    try:
        completed = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                                   encoding='utf-8', errors='replace', timeout=timeout)
        transcript = completed.stdout + '\n' + completed.stderr
        (OUT / filename).write_text(transcript, encoding='utf-8')
        return {'returncode': completed.returncode, 'timed_out': False,
                'last_lines': transcript.splitlines()[-16:], 'transcript': str(OUT / filename)}
    except subprocess.TimeoutExpired as exc:
        transcript = str(exc)
        (OUT / filename).write_text(transcript, encoding='utf-8')
        return {'returncode': None, 'timed_out': True, 'error': transcript,
                'transcript': str(OUT / filename)}


def main() -> int:
    files = sorted((ROOT / 'tests').glob('test_phase165*.py'))
    report = {'phase': '165 final targeted validation',
              'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'test_files': [str(f.relative_to(ROOT)) for f in files],
              'full_pytest_run': False,
              'retired_tests_restored': False,
              'production_modified': False}
    if not files:
        report['error'] = 'No current Phase 165 test files found'
    else:
        report['targeted_pytest'] = execute(
            [sys.executable, '-m', 'pytest', '-q', '-o', 'addopts=',
             *[str(f.relative_to(ROOT)) for f in files]],
            240, 'phase165_tests.txt')
    for n, k in ((2, 1), (3, 1), (3, 2)):
        # Separate interpreter ensures a failing/slow group cannot mask another.
        report[f'pi_{n+k}^{n}'] = execute(
            [sys.executable, str(Path(__file__).with_name('probe_goal.py')), str(n), str(k)],
            100, f'pi_{n+k}_{n}.txt')
    report['all_pass'] = (
        'targeted_pytest' in report and report['targeted_pytest']['returncode'] == 0
        and all(report[f'pi_{n+k}^{n}']['returncode'] == 0
                for n, k in ((2, 1), (3, 1), (3, 2))))
    (OUT / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('FULL PYTEST NOT RUN; proof completeness assessed separately per group')
    return 0 if report['all_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
