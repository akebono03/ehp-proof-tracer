from pathlib import Path
from datetime import datetime, timezone
import shutil

root = Path(__file__).resolve().parent.parent
target = root / 'tests' / 'test_phase150_rc4_5b_3_r1_beta_latex.py'
original = target.read_text(encoding='utf-8')
old = 'assert render_toda_expression_latex(beta) == r"\\\\beta"'
new = 'assert render_toda_expression_latex(beta) == r"\\beta"'
if original.count(old) != 1:
    if new in original and old not in original:
        print('ALREADY_PATCHED:', target)
        raise SystemExit(0)
    raise SystemExit('ABORT: expected original assertion was not found exactly once')
backup = root / 'phase167_r5_beta_test_fix_backup' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup.mkdir(parents=True)
shutil.copy2(target, backup / target.name)
target.write_text(original.replace(old,new),encoding='utf-8')
print('PATCHED:', target)
print('BACKUP:', backup / target.name)
