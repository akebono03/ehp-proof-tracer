"""Patch only two test input providers; fail closed on unexpected sources."""
from pathlib import Path
from datetime import datetime, timezone
import shutil

root = Path(__file__).resolve().parent.parent
backup = root / 'phase165_r6_audit_results' / 'runner_backup' / ('phase163_input_migration_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
files = {
    'tests/test_phase163_r4_r11_literature_registration.py': (
        '    existing_prop56_candidates,\n',
        '',
        'def _base_and_inputs():\n    return build_registry_bridge(), existing_prop56_candidates()\n',
        'def _base_and_inputs():\n    from phase165_r6_explicit_literature_inputs import prop56_inputs\n    return build_registry_bridge(), prop56_inputs()\n',
    ),
    'tests/test_phase163_r4_r12_literature_registration.py': (
        'def _inputs():\n    from phase163_r4_r12_literature_registration import existing_prop51_prop53_candidates\n    return existing_prop51_prop53_candidates()\n',
        'def _inputs():\n    from phase165_r6_explicit_literature_inputs import prop51_prop53_inputs\n    return prop51_prop53_inputs()\n',
        None,
        None,
    ),
}
planned = {}
for name, changes in files.items():
    path = root / name
    if not path.is_file():
        raise SystemExit(f'MISSING: {name}')
    original = path.read_text(encoding='utf-8')
    if name.endswith('r11_literature_registration.py'):
        before_import, after_import, before_func, after_func = changes
        if original.count(before_import) != 1 or original.count(before_func) != 1:
            raise SystemExit(f'SOURCE GUARD FAILED: {name}')
        updated = original.replace(before_import, after_import).replace(before_func, after_func)
    else:
        before_func, after_func, _, _ = changes
        if original.count(before_func) != 1:
            raise SystemExit(f'SOURCE GUARD FAILED: {name}')
        updated = original.replace(before_func, after_func)
    planned[name] = (original, updated)
helper = Path(__file__).resolve().parent / 'phase165_r6_explicit_literature_inputs.py'
if not helper.is_file():
    raise SystemExit('MISSING typed fixture source')
if (root/'phase165_r6_explicit_literature_inputs.py').exists():
    raise SystemExit('EXISTING typed fixture at destination: refusing overwrite')
backup.mkdir(parents=True, exist_ok=True)
for name,(original, updated) in planned.items():
    destination=backup/name
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(original,encoding='utf-8')
for name,(_, updated) in planned.items():
    (root/name).write_text(updated,encoding='utf-8')
    print('PATCHED:',name)
shutil.copy2(helper,root/'phase165_r6_explicit_literature_inputs.py')
print('ADDED: phase165_r6_explicit_literature_inputs.py')
print('BACKUP:',backup)
