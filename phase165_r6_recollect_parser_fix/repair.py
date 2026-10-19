"""Repair collected-error counts from an existing pytest log without rerunning pytest."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ERROR_HEADER = re.compile(
    r"^\s*_+\s+ERROR collecting\s+(?P<path>.+?)(?:\s+_+)?\s*$|^ERROR collecting\s+(?P<bare>\S.+?)\s*$",
    re.MULTILINE,
)
SUMMARY_COUNT = re.compile(r"\b(\d+)\s+errors?\s+in\s+[\d.]+s\b")


def parse_errors(content: str) -> list[str]:
    return sorted({(match.group('path') or match.group('bare')).strip() for match in ERROR_HEADER.finditer(content)})


def extract_summary_error_count(content: str) -> int | None:
    matches = SUMMARY_COUNT.findall(content)
    return int(matches[-1]) if matches else None


def repair_report(root: Path) -> dict:
    location = root / 'phase165_r6_audit_results' / 'recollection'
    log_path = location / 'collection.log'
    report_path = location / 'report.json'
    if not log_path.is_file() or not report_path.is_file():
        raise FileNotFoundError('Existing recollection/collection.log and report.json are required')
    log_text = log_path.read_text(encoding='utf-8', errors='replace')
    report = json.loads(report_path.read_text(encoding='utf-8'))
    parsed = parse_errors(log_text)
    count = extract_summary_error_count(log_text)
    if count is None:
        raise ValueError('pytest summary error count was not found; original report unchanged')
    if len(parsed) != count:
        raise ValueError(f'Header count {len(parsed)} differs from pytest summary {count}; original report unchanged')
    if report.get('exit_code') == 0 and count:
        raise ValueError('Collection result inconsistent; original report unchanged')
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = location / f'report.pre_parser_fix.{timestamp}.json'
    if backup.exists():
        raise FileExistsError(backup)
    shutil.copy2(report_path, backup)
    report['error_file_count'] = len(parsed)
    report['error_files'] = parsed
    report['pytest_summary_error_count'] = count
    report['parser_fix'] = {'status': 'REPAIRED_FROM_EXISTING_LOG', 'backup': str(backup), 'pytest_reexecuted': False}
    temp = report_path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(report_path)
    return {'error_file_count': len(parsed), 'pytest_summary_error_count': count, 'report': str(report_path), 'backup': str(backup), 'pytest_reexecuted': False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    result = repair_report(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
