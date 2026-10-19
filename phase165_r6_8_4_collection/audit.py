"""R6-8(4): targeted pytest collection audit only; no test bodies run."""
from __future__ import annotations
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / 'phase165_r6_audit_results' / 'collection_close' / 'r6_8_dependency_chains.json'
OUTPUT = ROOT / 'phase165_r6_audit_results' / 'r6_8_4_collection'

def run():
    if not BASELINE.is_file():
        raise SystemExit(f'MISSING BASELINE: {BASELINE}')
    data = json.loads(BASELINE.read_text(encoding='utf-8-sig'))
    records = data.get('test_dependencies')
    if not isinstance(records, list) or not records:
        raise SystemExit('Invalid baseline: test_dependencies absent')
    declared = data.get('failed_test_count')
    paths = sorted({record['test_path'] for record in records if isinstance(record, dict) and isinstance(record.get('test_path'), str)})
    if not paths:
        raise SystemExit('No target test paths in baseline')
    present = [p for p in paths if (ROOT / p).is_file()]
    absent = [p for p in paths if not (ROOT / p).is_file()]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, '-m', 'pytest', '--collect-only', '-q', '--continue-on-collection-errors', '--tb=short', '-o', 'addopts=', *present]
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, errors='replace') if present else None
    transcript = result.stdout if result else 'No listed target tests remain.\n'
    (OUTPUT / 'collection.txt').write_text(transcript, encoding='utf-8')
    match = re.findall(r'(?m)^=+\s*(\d+) errors? in [\d.]+s\s*=+\s*$', transcript)
    error_count = int(match[-1]) if match else None
    summaries = [line.strip() for line in transcript.splitlines() if line.startswith('ERROR ') or line.startswith('FAILED ')]
    report = {
        'phase': '165 R6-8(4)', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'baseline_error_records': declared, 'baseline_test_paths': len(paths),
        'existing_test_paths': len(present), 'missing_test_paths': absent,
        'command': command, 'returncode': result.returncode if result else None,
        'collection_error_count_from_summary': error_count,
        'error_summary_lines': summaries,
        'transcript_path': str(OUTPUT / 'collection.txt'),
        'test_bodies_executed': False, 'full_pytest_executed': False,
        'source_files_modified': False,
        'interpretation': 'Baseline describes static dependency chains; collection errors must be measured separately.',
    }
    (OUTPUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('R6-8(4) targeted collection complete; no test bodies executed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(run())
