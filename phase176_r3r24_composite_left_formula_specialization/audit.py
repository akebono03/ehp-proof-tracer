"""Phase 176 R3R24 narrowly installs a typed left-composite formula guard."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone
from phase176_r3r24_composite_left_formula_specialization.installer import install

PACKAGE = 'phase176_r3r24_composite_left_formula_specialization'
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    record: dict[str, object] = {'phase': '176_R3R24', 'gate': 'FAIL_R3R24', 'full_pytest': 'NOT_RUN', 'new_given': 0, 'new_mathematical_rules': 0, 'timestamp_utc': datetime.now(timezone.utc).isoformat()}
    try:
        record.update(install(args.dry_run))
        record['gate'] = 'PASS_R3R24_DRYRUN' if args.dry_run else 'PASS_R3R24_PATCH_INSTALLED_TESTS_PENDING'
    except Exception as error:
        record['error'] = type(error).__name__ + ': ' + str(error)
    root = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    root.mkdir(parents=True, exist_ok=True)
    report = root / 'report.json'
    report.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE176_R3R24_GATE=' + str(record['gate']))
    print('PHASE176_R3R24_HEAD=' + str(record.get('head', 'UNVERIFIED')))
    print('PHASE176_R3R24_REPORT=' + str(report))
    if 'error' in record:
        print('PHASE176_R3R24_ERROR=' + str(record['error']))
    print('PHASE176_R3R24_FULL_PYTEST=NOT_RUN')
    print('(END)')
    return 0 if str(record['gate']).startswith('PASS_') else 1
if __name__ == '__main__':
    sys.exit(main())
