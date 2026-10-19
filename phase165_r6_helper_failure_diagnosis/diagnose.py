"""Summarize the most recent failed historical helper recovery; read only."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re

PATTERNS = (
    ('missing_module', re.compile(r"(?:ModuleNotFoundError: No module named|No module named) ['\"]([^'\"]+)['\"]")),
    ('missing_export', re.compile(r"ImportError: cannot import name ['\"]([^'\"]+)['\"] from ['\"]([^'\"]+)['\"]")),
    ('failed_assertions', re.compile(r"(?m)^FAILED\s+([^\n]+)")),
    ('errors', re.compile(r"(?m)^ERROR\s+([^\n]+)")),
)

def summarize(report: dict, log: str) -> dict:
    found = {}
    for key, pattern in PATTERNS:
        found[key] = sorted({ '|'.join(match) if isinstance(match, tuple) else match for match in pattern.findall(log)})
    summary_lines = [line.strip() for line in log.splitlines() if re.search(r'\d+ (?:failed|error|passed|skipped|warnings?)', line)]
    relevant = [line for line in log.splitlines() if any(part in line for part in ('E   ', 'ImportError:', 'ModuleNotFoundError:', 'FAILED ', 'ERROR ', 'AssertionError:', 'NameError:', 'AttributeError:', 'TypeError:'))]
    return {'recovery_status': report.get('status'), 'candidate_count': len(report.get('candidates', [])), 'candidate_results': report.get('candidates', []), 'detected_issues': found, 'pytest_summaries': summary_lines[-8:], 'error_excerpt': relevant[-80:], 'test_log_available': bool(log.strip()), 'changes_made': False, 'full_pytest_run': False}

def newest_report(root: Path) -> Path | None:
    parent = root / 'phase165_r6_audit_results' / 'helper_recovery'
    candidates = list(parent.glob('*/report.json')) if parent.is_dir() else []
    return max(candidates, key=lambda x: x.parent.name) if candidates else None

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    report_path = newest_report(root)
    if report_path is None:
        print('ERROR: no helper_recovery/*/report.json found. No files changed.')
        return 2
    try:
        report = json.loads(report_path.read_text(encoding='utf-8-sig'))
    except (ValueError, OSError) as exc:
        print(f'ERROR: could not read {report_path}: {exc}')
        return 2
    log_path = report_path.with_name('targeted_pytest.log')
    log = log_path.read_text(encoding='utf-8', errors='replace') if log_path.exists() else ''
    result = summarize(report, log)
    result['source_report'] = str(report_path)
    result['source_log'] = str(log_path) if log_path.is_file() else None
    output = root / 'phase165_r6_audit_results' / 'helper_failure_diagnosis' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'diagnosis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': result['recovery_status'], 'detected_issues': result['detected_issues'], 'pytest_summaries': result['pytest_summaries'], 'error_excerpt': result['error_excerpt'][-25:], 'output': str(output / 'diagnosis.json'), 'pytest_executed': False}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
