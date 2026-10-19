"""Read-only classification of the latest 266 pytest collection errors."""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HEADER = re.compile(r'^\s*_+\s+ERROR collecting\s+(.+?)\s+_+\s*$', re.M)
SUMMARY = re.compile(r'(\d+) errors? in [\d.]+s')
EXCEPTION = re.compile(r'^\s*(?:E\s+)?(ImportError|ModuleNotFoundError|AttributeError|NameError|SyntaxError):\s*(.+)$', re.M)
MISSING_MODULE = re.compile(r"No module named ['\"]([^'\"]+)['\"]")
MISSING_SYMBOL = re.compile(r"cannot import name ['\"]([^'\"]+)['\"] from ['\"]([^'\"]+)['\"]")
ROOT_DIR = 'phase165_r6_audit_results/graph_cleanup'

def extract_errors(log: str) -> list[dict]:
    headers = list(HEADER.finditer(log))
    rows = []
    for i, h in enumerate(headers):
        block = log[h.end():headers[i + 1].start() if i + 1 < len(headers) else len(log)]
        exceptions = EXCEPTION.findall(block)
        if exceptions:
            kind, message = exceptions[-1]
        else:
            kind, message = 'UNKNOWN', 'No exception line found'
        missing = MISSING_MODULE.search(message)
        symbol = MISSING_SYMBOL.search(message)
        if missing:
            blocker, reason = missing.group(1), 'missing_module'
        elif symbol:
            blocker, reason = symbol.group(2) + ':' + symbol.group(1), 'missing_export'
        else:
            blocker, reason = message, 'other'
        path = h.group(1).strip().replace('\\', '/')
        phase_match = re.search(r'test_phase(\d+)', path)
        phase = int(phase_match.group(1)) if phase_match else None
        rows.append({'file': path, 'phase': phase, 'reason': reason, 'exception_type': kind, 'message': message, 'blocker': blocker})
    return rows

def categorize(row: dict) -> str:
    blocker = row['blocker']
    if blocker.startswith('tests.test_phase143_19_method_evidence') or blocker.startswith('test_phase143_19_method_evidence'):
        return 'MISSING_SHARED_TEST_HELPER'
    if blocker.startswith('test_phase144_') or blocker.startswith('tests.test_phase144_'):
        return 'MISSING_HISTORICAL_TEST_HELPER'
    if blocker.startswith('probes.') or blocker.startswith('toda_rules:toda_pi4_3_delta_image_free_cyclic_inference_rule'):
        return 'RETIRED_PROBE_RULE'
    if blocker.startswith(('repository_inference', 'repository_element_', 'repository_generator_', 'repository_known_')):
        return 'RETIRED_REPOSITORY'
    if blocker.startswith('toda_group_proof_generic_narrative_renderer'):
        return 'RETIRED_RENDERER'
    if row['reason'] == 'missing_module':
        return 'OTHER_MISSING_MODULE'
    if row['reason'] == 'missing_export':
        return 'OTHER_MISSING_EXPORT'
    return 'OTHER_ERROR'

def make_report(log: str, source: str) -> dict:
    rows = extract_errors(log)
    summary = SUMMARY.findall(log)
    if not summary:
        raise ValueError('Missing pytest collection summary')
    reported = int(summary[-1])
    if reported != len(rows):
        raise ValueError(f'Collection mismatch: reported={reported}, parsed={len(rows)}')
    if len({r['file'] for r in rows}) != len(rows):
        raise ValueError('Duplicate file in collection results')
    for row in rows:
        row['category'] = categorize(row)
        row['action'] = 'REVIEW_REQUIRED_NO_AUTOMATIC_DELETION'
    cats = Counter(row['category'] for row in rows)
    blockers = defaultdict(list)
    for row in rows:
        blockers[row['blocker']].append(row['file'])
    return {'status':'READ_ONLY_NO_PYTEST', 'source':source, 'error_count':reported,
            'category_counts':dict(sorted(cats.items(), key=lambda v: (-v[1], v[0]))),
            'blockers':[{'blocker':k,'count':len(v),'files':v} for k,v in sorted(blockers.items(),key=lambda p:(-len(p[1]),p[0]))],
            'records':rows}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    previous = root/ROOT_DIR
    sessions = sorted([p for p in previous.iterdir() if (p/'collection.log').is_file()]) if previous.exists() else []
    if not sessions:
        raise SystemExit('No graph_cleanup collection.log found; nothing changed')
    source = sessions[-1]/'collection.log'
    report = make_report(source.read_text(encoding='utf-8',errors='replace'),str(source))
    if report['error_count'] != 266:
        raise SystemExit(f'Expected 266 errors, found {report["error_count"]}; no files changed')
    output = root/'phase165_r6_audit_results'/'triage_266'
    output.mkdir(parents=True,exist_ok=True)
    (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines = ['# Phase 165 R6: 266 Collection Errors','', 'Read-only results. No test or production source changed.','', '| Category | Count |','|---|---:|']
    for k,v in report['category_counts'].items():
        lines.append(f'| {k} | {v} |')
    lines.extend(['','## Top blockers',''])
    for b in report['blockers'][:30]:
        lines.append(f'- `{b["blocker"]}`: {b["count"]} files')
    lines.extend(['','## Boundary','','Do not restore retired group-specific APIs or renderers. Preserve current proof-search, mathematical and web-output tests. No test files were removed.'])
    (output/'summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Errors:',report['error_count'])
    for k,v in report['category_counts'].items(): print(f'{v:4d} {k}')
    print('Report:',output/'report.json')
    print('No pytest run, no deletion, phase closure PENDING.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
