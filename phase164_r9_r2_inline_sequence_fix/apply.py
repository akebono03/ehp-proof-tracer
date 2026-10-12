"""Apply Phase 164 R9-R2 helper correction, run focused pytest and live audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OLD_SHA = '6dfbd042d10aef7cc38d3066d8f2a7e808366476195cd35d5d0ef64d382b1d5f'
TARGET = 'phase164_r9_narrative_contract.py'
RENDERER = 'toda_group_proof_narrative_renderer.py'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    package = Path(__file__).resolve().parent
    target = root / TARGET
    renderer = root / RENDERER
    if not target.exists() or not renderer.exists():
        raise FileNotFoundError('Phase 164 R9 prior install not found; no modification')
    source = target.read_bytes()
    replacement = (package / TARGET).read_bytes()
    if 'normalize_public_narrative_contract' not in renderer.read_text(encoding='utf-8'):
        raise RuntimeError('Renderer is not connected to R9 normalizer; no modification')
    state = 'already_applied' if sha(source) == sha(replacement) else ('ready' if sha(source) == OLD_SHA else 'unexpected_source')
    audit = {'phase': '164 R9-R2', 'state': state, 'changed_files': [TARGET],
             'proof_tree_modified': False, 'full_pytest_run': False,
             'original_r9_bug': 'the normalizer inspected display math but did not inspect $...$ inline math'}
    if args.dry_run:
        print(json.dumps(audit, ensure_ascii=False, indent=2))
        if state == 'unexpected_source':
            raise RuntimeError('R9 source is locally modified; no replacement allowed')
        return
    if state == 'unexpected_source':
        raise RuntimeError('unexpected R9 normalizer SHA256; no changes made')
    backup = None
    if state == 'ready':
        backup = root / ('phase164_r9_r2_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
        backup.mkdir()
        shutil.copy2(target, backup / TARGET)
        target.write_bytes(replacement)
        audit['backup_dir'] = str(backup)
    output = root / 'phase164_r9_r2_output'
    output.mkdir(exist_ok=True)
    try:
        tests = [str(package / 'test_phase164_r9_r2.py')]
        old_test = root / 'phase164_r9_web_narrative' / 'test_phase164_r9_narrative_contract.py'
        if old_test.is_file():
            tests.append(str(old_test))
        existing_test = root / 'tests' / 'test_phase164_r5_web_registry_connection.py'
        if not existing_test.is_file():
            raise RuntimeError('R5 Web regression test is missing')
        tests.append(str(existing_test))
        result = subprocess.run([sys.executable, '-m', 'pytest', '-q', *tests], cwd=root)
        audit['focused_pytest_returncode'] = result.returncode
        if result.returncode != 0:
            raise RuntimeError('targeted pytest failure; rolled back')
        probe = subprocess.run([sys.executable, str(package / 'probe_web_narrative.py'), str(output)], cwd=root)
        audit['live_web_probe_returncode'] = probe.returncode
        if probe.returncode != 0:
            raise RuntimeError('live Web narrative remains unverified; rolled back')
        audit['status'] = 'R9_R2_TARGETED_AND_RUNTIME_PASS'
        (output / 'CHANGED_CODE.md').write_text(
            '# Phase 164 R9-R2 変更コード全文\n\n'
            '変更対象: ' + TARGET + ' の全関数、import 全文。\n\n```python\n'
            + replacement.decode('utf-8') + '\n```\n\n'
            '追加テスト: test_phase164_r9_r2.py（全文）。\n\n```python\n'
            + (package / 'test_phase164_r9_r2.py').read_text(encoding='utf-8')
            + '\n```\n', encoding='utf-8')
        (output / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(audit, ensure_ascii=False, indent=2))
    except Exception:
        if backup is not None:
            shutil.copy2(backup / TARGET, target)
        raise


if __name__ == '__main__':
    main()
