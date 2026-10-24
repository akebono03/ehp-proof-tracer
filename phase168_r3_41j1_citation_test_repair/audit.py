"""R3-41J1: R3-41I quality audit rerun in an isolated output directory."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase168_r3_41i_renderer_closure_audit.audit import run_audit


def main() -> int:
    folder = Path(__file__).resolve().parent / 'output'
    report = run_audit(output=folder)
    for row in report['cases']:
        print(row['name'], 'remaining_unused_references', row['references_not_explicitly_tagged_in_proof'],
              'benchmark_gaps', row['missing_benchmark_explanations'],
              'proof_diff', row['proof_difference_lines'],
              'reference_diff', row['reference_difference_lines'])
    print('STATUS', report['status'])
    print('REPORT', folder / 'audit.md')
    print('REVIEW_BUNDLE', folder / 'review_bundle.zip')
    print('PHASE168_FULL_PYTEST_RUN', False)
    if report['errors'] or not all(report['route_contract'].values()):
        return 1
    if any(row['references_not_explicitly_tagged_in_proof'] or
           row['missing_benchmark_explanations'] or row['missing_body_locators']
           for row in report['cases']):
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
