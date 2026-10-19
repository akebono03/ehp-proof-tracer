"""Read-only consolidation of Phase 165 failed pytest nodes and live test sources."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / 'failed_test_list.csv'
OUT = ROOT / 'phase165_r6_audit_results' / 'consolidated_triage'


def classify(relative_path: str, body: str) -> tuple[str, str]:
    name = Path(relative_path).name
    if name.startswith('test_phase103_'):
        indicators = ('standard_production_applicability_catalog', '_phase103_6d', '1188', '267')
        if any(marker in body for marker in indicators) and ('catalog' in body or 'relevance_category' in body):
            return ('LEGACY_CANDIDATE', 'Retired applicability catalog; verify equivalent current coverage before archival')
        return ('MANUAL_REVIEW', 'Phase 103 with no confident catalog-only signature')
    if name.startswith('test_phase163_'):
        if 'existing_prop51_prop53_candidates' in body or 'existing_prop56_candidates' in body:
            return ('MIGRATE_FIXTURES', 'Replace legacy historical candidate extraction with explicit typed fixtures')
        return ('MANUAL_REVIEW', 'Phase 163 assertions need typed registration review')
    if name.startswith('test_phase164_'):
        return ('MIGRATE_WEB_TEST', 'Review tests against new search/replay entry; preserve assertion coverage')
    if name.startswith('test_phase165_'):
        return ('CURRENT_REGRESSION', 'Phase 165 contract: rerun focused tests after recent fixes')
    if name.startswith('test_phase56_'):
        return ('DEPENDENCY_FAILURE', 'Phase 56 proof-chain failure; check first IndexError and typed source')
    return ('MANUAL_REVIEW', 'Do not retire without separate evidence')


def main() -> int:
    if not MANIFEST.exists():
        raise SystemExit(f'Missing manifest: {MANIFEST}')
    records = []
    with MANIFEST.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        relative_path = row['file'].replace('\\', '/')
        source = ROOT / relative_path
        if not source.is_file():
            status, reason, digest = 'MISSING_SOURCE', 'Local test source not found; no action possible', None
        else:
            data = source.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            status, reason = classify(relative_path, data.decode('utf-8', errors='replace'))
        records.append(dict(row, triage=status, reason=reason, source_sha256=digest or ''))
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'failed_nodes_triage.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    by_source = defaultdict(list)
    for item in records:
        by_source[item['file']].append(item)
    with (OUT / 'failed_files_triage.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file','failed_tests','triage','source_sha256','reason'])
        writer.writeheader()
        for name, items in sorted(by_source.items()):
            first = items[0]
            writer.writerow(dict(file=name,failed_tests=len(items),triage=first['triage'],source_sha256=first['source_sha256'],reason=first['reason']))
    counts = Counter(x['triage'] for x in records)
    summary = {'total_failed_nodes':len(records),'affected_files':len(by_source),'by_triage':dict(sorted(counts.items())),'modified_repository_files':0,'archived_files':0,'full_pytest_run':False,'warning':'Candidate status is NOT proof of retirement safety. Coverage equivalence requires review.'}
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('REPORT_DIR:', OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
