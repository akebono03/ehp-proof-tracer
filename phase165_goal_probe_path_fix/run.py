"""Run three Phase 165 goal probes with repository-root imports enabled."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase165_r6_audit_results' / 'goal_probe_path_fix'


def probe_group(n: int, k: int) -> dict:
    environment = dict(os.environ)
    previous_path = environment.get('PYTHONPATH', '')
    environment['PYTHONPATH'] = str(ROOT) + (os.pathsep + previous_path if previous_path else '')
    command = [sys.executable, str(Path(__file__).with_name('probe_goal.py')), str(n), str(k)]
    filename = OUT / f'pi_{n+k}_{n}.txt'
    try:
        result = subprocess.run(
            command, cwd=ROOT, env=environment, capture_output=True,
            encoding='utf-8', errors='replace', text=True, timeout=100,
        )
        transcript = result.stdout + '\n' + result.stderr
        filename.write_text(transcript, encoding='utf-8')
        return {
            'returncode': result.returncode,
            'timed_out': False,
            'output': transcript.strip()[-10000:],
            'transcript': str(filename),
        }
    except subprocess.TimeoutExpired as exc:
        filename.write_text(str(exc), encoding='utf-8')
        return {'returncode': None, 'timed_out': True, 'error': str(exc), 'transcript': str(filename)}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        'phase': '165 goal probe path correction',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'root': str(ROOT),
        'production_modified': False,
        'pytest_executed': False,
        'prior_targeted_tests': '68 passed (previous user run; not rerun)',
    }
    for n, k in ((2, 1), (3, 1), (3, 2)):
        report[f'pi_{n+k}^{n}'] = probe_group(n, k)
    report['all_complete'] = all(
        report[f'pi_{n+k}^{n}']['returncode'] == 0
        for n, k in ((2, 1), (3, 1), (3, 2))
    )
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('No full pytest run; goal search states are not mathematical certification.')
    return 0 if report['all_complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
