from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / 'phase165_r3_recursive_search.py'
src = FILE.read_text(encoding='utf-8')
needle = '    if lookup_mode not in ("legacy", "typed_reference"):\n'
replacement = '    if lookup_mode not in ("legacy", "typed_reference", "typed_reference_ordered"):\n'
assert src.count(needle) == 1, 'unexpected lookup-mode definition'
src = src.replace(needle, replacement)
needle = '''            if lookup_mode == "typed_reference":
                options = list(_typed_reference_steps(bridge, target))
            else:
'''
replacement = '''            if lookup_mode == "typed_reference_ordered":
                from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
                options = list(ordered_typed_reference_steps(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                ))
            elif lookup_mode == "typed_reference":
                options = list(_typed_reference_steps(bridge, target))
            else:
'''
assert src.count(needle) == 1, 'unexpected lookup branch'
src = src.replace(needle, replacement)
needle = '            if lookup_mode == "typed_reference" and len(options) == 1:\n'
replacement = '            if lookup_mode in ("typed_reference", "typed_reference_ordered") and len(options) == 1:\n'
assert src.count(needle) == 1, 'R13-R1 direct priority change missing'
src = src.replace(needle, replacement)
backup = FILE.with_suffix('.py.r52_r15_backup')
if not backup.exists():
    shutil.copy2(FILE, backup)
FILE.write_text(src, encoding='utf-8')
print('R52-R15 strict ordered typed-reference lookup installed')
