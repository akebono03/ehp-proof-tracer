from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'phase165_r6_audit_results' / 'closure_check'
OUTPUT.mkdir(parents=True, exist_ok=True)


def run_pytest(args: list[str], filename: str) -> dict:
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    command = [sys.executable, '-m', 'pytest', *args]
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors='replace', timeout=900, env=env)
        return {'command': command, 'returncode': result.returncode, 'stdout': result.stdout[-250000:], 'stderr': result.stderr[-30000:]}
    except subprocess.TimeoutExpired as error:
        return {'command': command, 'returncode': -1, 'stdout': str(error.stdout or '')[-5000:], 'stderr': 'Timed out after 900 seconds'}


def main() -> int:
    report: dict = {
        'phase': '165 R6 closure check',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'mode': 'READ_ONLY_NO_DELETIONS',
        'full_pytest_run': False,
        'root': str(ROOT),
    }
    old_reports = sorted((ROOT / 'phase165_r6_audit_results').glob('old_proof_retirement/*/report.json'))
    report['previous_retirement_report'] = str(old_reports[-1]) if old_reports else None
    if old_reports:
        try:
            report['previous_retirement_summary'] = json.loads(old_reports[-1].read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            report['previous_retirement_report_error'] = str(exc)
    collect = run_pytest(['--collect-only', '-q'], 'collection')
    (OUTPUT / 'collection.stdout.txt').write_text(collect['stdout'], encoding='utf-8')
    (OUTPUT / 'collection.stderr.txt').write_text(collect['stderr'], encoding='utf-8')
    report['collection'] = {
        'returncode': collect['returncode'],
        'error_lines': [line for line in collect['stdout'].splitlines() if re.search(r'ERROR collecting|ImportError|ModuleNotFoundError|SyntaxError|errors? in ', line, re.I)][-200:],
        'tail': collect['stdout'][-2000:],
    }
    candidates = sorted(p for p in ROOT.glob('test_phase165*.py') if p.is_file())
    report['top_level_phase165_test_file_count'] = len(candidates)
    # Focus on tests exercising the currently shared proof/search/renderer path.
    tokens = ('r52', 'r57', 'backward', 'common_renderer', 'shared_math')
    selected = [p for p in candidates if any(t in p.name.lower() for t in tokens)][:12]
    report['focused_test_files'] = [p.name for p in selected]
    if selected:
        focus = run_pytest(['-q', '--maxfail=1', *[p.name for p in selected]], 'focused')
        (OUTPUT / 'focused.stdout.txt').write_text(focus['stdout'], encoding='utf-8')
        (OUTPUT / 'focused.stderr.txt').write_text(focus['stderr'], encoding='utf-8')
        report['focused'] = {'returncode': focus['returncode'], 'tail': focus['stdout'][-3000:]}
    else:
        report['focused'] = {'returncode': None, 'reason': 'No matching top-level test files; no claim of passing tests'}
    (OUTPUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'mode': report['mode'], 'collection_returncode': report['collection']['returncode'], 'collection_error_lines': report['collection']['error_lines'][-20:], 'focused_test_files': report['focused_test_files'], 'focused_returncode': report['focused']['returncode'], 'report': str(OUTPUT / 'report.json'), 'full_pytest_run': False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
