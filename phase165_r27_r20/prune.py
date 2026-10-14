"""R27-R20: guarded removal of obsolete root Python backup files only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys

BACKUP_CANDIDATES = (
    'phase164_r5_web_registry_connection.phase164_r5_r1_backup.py',
    'phase164_r7_r3_generator_registry.phase164_r7_r4_backup.py',
    'repository_generator_known_group_identity_lookup.phase164_r7_r3_backup.py',
    'repository_operation_query_facade.phase164_r7_r4_backup.py',
    'toda_calculation_facade.phase164_r7_r5_backup.py',
    'web_group_proof.phase164_r5_backup.py',
    'web_group_proof.phase164_r5_r1_backup.py',
    'web_group_proof.phase164_r5_r2_backup.py',
    'web_group_proof.phase164_r5_r3_backup.py',
    'web_group_proof.phase165_r39_backup.py',
    'web_group_proof.phase165_r40_backup.py',
    'web_group_proof.phase165_r52_r3_backup.py',
    'web_group_proof.phase165_r52_r3_empty_steps_backup.py',
)
PROTECTED = ('standard_production_repository.py', 'standard_repository.py',
             'proof_repository.py', 'toda_prop515_upper_bootstrap.py',
             'toda_calculation_facade.py', 'main.py', 'web_app.py')


def prune(root: Path, *, apply: bool, output: Path) -> dict:
    root = root.resolve()
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    backup_dir = output / 'removed_files_backup'
    records = []
    for name in BACKUP_CANDIDATES:
        target = root / name
        record = {'path': name, 'status': 'ABSENT'}
        if not target.is_file() or target.is_symlink():
            records.append(record)
            continue
        # Guard against arbitrary edits to the file names we expect to be historical backups.
        if '_backup.py' not in name or name in PROTECTED:
            record['status'] = 'PROTECTED'
            records.append(record)
            continue
        # Check executable root code references to the full backup filename.
        consumers = []
        for source in root.glob('*.py'):
            if source.name == name or source.name in BACKUP_CANDIDATES:
                continue
            try:
                body = source.read_text(encoding='utf-8-sig')
            except (UnicodeError, OSError):
                consumers.append(source.name + ':unreadable')
                continue
            if name in body:
                consumers.append(source.name)
        if consumers:
            record['status'] = 'BLOCKED_BY_ROOT_REFERENCE'
            record['consumers'] = sorted(consumers)
        elif apply:
            backup_dir.mkdir(exist_ok=True)
            backup = backup_dir / name
            if backup.exists():
                if backup.read_bytes() != target.read_bytes():
                    record['status'] = 'BLOCKED_BACKUP_COLLISION'
                    records.append(record)
                    continue
            else:
                shutil.copy2(target, backup)
            if backup.read_bytes() != target.read_bytes():
                raise RuntimeError(f'Backup verification failed: {name}')
            target.unlink()
            record['status'] = 'REMOVED_WITH_BACKUP'
        else:
            record['status'] = 'ELIGIBLE_NOT_REMOVED'
        records.append(record)
    report = {
        'phase': '165 R27-R20',
        'mode': 'GUARDED_LEGACY_ROOT_BACKUP_REMOVAL',
        'apply': apply,
        'removed_files': sum(x['status'] == 'REMOVED_WITH_BACKUP' for x in records),
        'blocked_files': sum(x['status'].startswith('BLOCKED') for x in records),
        'production_core_modified': False,
        'full_pytest_run': False,
        'bootstrap_deleted': False,
        'remaining_core_blockers': ['toda_calculation_facade.py', 'repository_proof_scope_facade.py', 'repository_generator_known_group_identity_lookup.py'],
        'records': records,
    }
    (output / 'audit_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    report = prune(args.root, apply=args.apply, output=args.output)
    print(json.dumps({key: val for key, val in report.items() if key != 'records'}, ensure_ascii=False, indent=2))
    print('Report:', args.output / 'audit_report.json')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
