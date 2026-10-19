"""Collect current tests without executing test bodies or modifying source files."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def select_paths(root: Path) -> list[str]:
    paths: list[str] = []
    if (root / 'tests').is_dir():
        paths.append('tests')
    paths.extend(path.name for path in sorted(root.glob('test_*.py')) if path.is_file())
    if not paths:
        raise ValueError('No active test directories or root test files')
    return paths


def parse_errors(content: str) -> list[str]:
    pattern = re.compile(r'^ERROR collecting (.+?)(?:\s+_+)?$', re.MULTILINE)
    return sorted(set(match.strip() for match in pattern.findall(content)))


def run(root: Path) -> int:
    if not (root / 'phase165_r52_r4_flask_bridge.py').is_file():
        raise ValueError('Please run from the ehp_proof project root')
    output = root / 'phase165_r6_audit_results' / 'recollection'
    output.mkdir(parents=True, exist_ok=True)
    log = output / 'collection.log'
    report = output / 'report.json'
    paths = select_paths(root)
    command = [sys.executable, '-m', 'pytest', '--collect-only', '-q', '--continue-on-collection-errors', *paths]
    environment = os.environ.copy()
    environment['PYTHONPATH'] = str(root) + os.pathsep + environment.get('PYTHONPATH', '')
    started = datetime.now(timezone.utc).isoformat()
    code = 130
    interrupted = False
    with log.open('w', encoding='utf-8') as stream:
        stream.write('RUN: ' + repr(command) + '\n')
        stream.flush()
        process = subprocess.Popen(command, cwd=root, env=environment, stdout=stream, stderr=subprocess.STDOUT)
        try:
            code = process.wait()
        except KeyboardInterrupt:
            interrupted = True
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    content = log.read_text(encoding='utf-8', errors='replace')
    errors = parse_errors(content)
    summary_lines = [line.strip() for line in content.splitlines() if re.search(r'\b(?:errors?|tests? collected|deselected)\b', line) and (' in ' in line or 'collected' in line)]
    data = {'timestamp_utc': started, 'scope': paths, 'command': command, 'exit_code': code, 'interrupted': interrupted, 'error_file_count': len(errors), 'error_files': errors, 'summary_tail': summary_lines[-8:], 'log_path': str(log), 'status': 'PASS' if code == 0 and not errors else ('INTERRUPTED' if interrupted else 'PENDING'), 'test_bodies_executed': False, 'baseline_before_cleanup_collection_errors': 497, 'historical_deleted_test_files': 117}
    temporary = report.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(report)
    print('Collection exit code:', code)
    print('Error files found:', len(errors))
    for line in data['summary_tail']:
        print('Summary:', line[:240])
    print('Report:', report)
    print('Log:', log)
    print('No test bodies executed; full pytest NOT run; Phase closure PENDING unless separately verified.')
    return 0 if not interrupted else 130


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    return run(args.root.resolve())


if __name__ == '__main__':
    raise SystemExit(main())
