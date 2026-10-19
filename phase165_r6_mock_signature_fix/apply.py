from __future__ import annotations

import ast
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    root = Path.cwd()
    target = root / 'test_phase165_r52_r2_search_adapter.py'
    production = root / 'phase165_r52_r2_search_adapter.py'
    if not target.is_file() or not production.is_file():
        raise SystemExit('Run from the ehp_proof repository root; required files missing.')

    old = 'def fake_reconstruct(goal, bridge, cite, provider, *, verified_assertion_ids, lookup_mode, progress_observer):'
    new = 'def fake_reconstruct(goal, bridge, cite, provider, *, verified_assertion_ids, lookup_mode, progress_observer, completed_internal_proofs):'
    source = target.read_text(encoding='utf-8')
    prod_source = production.read_text(encoding='utf-8')
    if 'completed_internal_proofs=completed_internal_proofs' not in prod_source:
        raise SystemExit('Current production contract differs from audited GitHub version; no changes made.')
    if source.count(old) != 3:
        if source.count(new) == 3 and source.count(old) == 0:
            print('ALREADY_APPLIED: three fake_reconstruct functions accept completed_internal_proofs')
        else:
            raise SystemExit(f'Unexpected test code: old signatures={source.count(old)}, new signatures={source.count(new)}; no changes made.')
    else:
        updated = source.replace(old, new)
        ast.parse(updated, filename=str(target))
        backup_dir = root / 'phase165_r6_audit_results' / 'runner_backup'
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup = backup_dir / f'test_phase165_r52_r2_search_adapter_{stamp}.py'
        shutil.copy2(target, backup)
        target.write_text(updated, encoding='utf-8')
        print(f'PATCHED: {target}')
        print(f'BACKUP: {backup}')
    args = [sys.executable, '-m', 'pytest', '-q', '-o', 'addopts=',
            'test_phase165_r52_r2_search_adapter.py::test_r52_r2_partial_preserves_proved_leaf',
            'test_phase165_r52_r2_search_adapter.py::test_r52_r2_no_steps_is_failed',
            'test_phase165_r52_r2_search_adapter.py::test_r52_r2_canonical_success_is_complete_only_for_target']
    print('Running three targeted tests; full suite is NOT run.', flush=True)
    return subprocess.call(args, cwd=root)


if __name__ == '__main__':
    raise SystemExit(main())
