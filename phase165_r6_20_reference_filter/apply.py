from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'toda_group_proof_narrative_references.py'
OLD = '''      if boundary.component_key is None:
        fixed_components = (
          get_toda_fixed_statement_components(
            boundary.reference_locator
          )
        )

        if fixed_components:
          retained_steps.append(
            proof_step
          )

        continue
'''
NEW = '''      if boundary.component_key is None:
        # An aggregate without a registered component is not a
        # validated fixed statement eligible for public citation.
        continue
'''

def run():
    if not TARGET.is_file():
        raise SystemExit(f'Missing source: {TARGET}')
    before = TARGET.read_bytes()
    text = before.decode('utf-8')
    if text.count(OLD) != 1:
        raise SystemExit('ABORT: expected reference-filter block is not unique or absent; no files changed')
    updated = text.replace(OLD, NEW, 1)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT / 'phase165_r6_audit_results' / 'r6_20_reference_filter' / stamp
    out.mkdir(parents=True, exist_ok=False)
    shutil.copy2(TARGET, out / TARGET.name)
    TARGET.write_bytes(updated.encode('utf-8'))
    print('APPLIED:', TARGET)
    print('BACKUP:', out / TARGET.name)
    tests = ['tests/test_phase157_r5_r4_generic_reference_selection.py',
             'tests/test_phase157_r2_literature_statement_boundary.py',
             'tests/test_phase157_r4_r3_reference_selection_integration.py',
             'tests/test_phase157_r5_r3_boundary_catalog_expansion.py',
             'tests/test_phase156_r5_repair4_bridge_reference_inference.py']
    cmd = [sys.executable, '-m', 'pytest', '-q', *tests]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    (out / 'pytest_stdout.txt').write_text(proc.stdout, encoding='utf-8')
    (out / 'pytest_stderr.txt').write_text(proc.stderr, encoding='utf-8')
    print(proc.stdout[-6500:])
    if proc.stderr:
        print(proc.stderr[-1200:])
    report = {'phase':'165 R6-20','status':'TARGETED_PASS' if proc.returncode == 0 else 'TARGETED_FAILED_REVIEW_REQUIRED',
        'modified_file':TARGET.name,'changed_function':'filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary',
        'backup':str(out / TARGET.name),'before_sha256':hashlib.sha256(before).hexdigest(),
        'after_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),
        'pytest_returncode':proc.returncode,'full_pytest_run':False}
    (out / 'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    raise SystemExit(proc.returncode)

if __name__=='__main__':
    run()
