"""R16-R2: preserve nullable migration records during bridge merge."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
target = root / "phase165_r52_r9_shared_math.py"
if not target.is_file():
    raise SystemExit("Repository target not found; no changes made")
source = target.read_text(encoding="utf-8")
old = 'records.extend(replace(record, assertion_id=prefix + record.assertion_id) for record in source.records)'
new = 'records.extend(\n            replace(record, assertion_id=prefix + record.assertion_id)\n            if record.assertion_id is not None else record\n            for record in source.records\n        )'
if source.count(old) == 1:
    updated = source.replace(old, new)
    compile(updated, str(target), "exec")
    backup = root / "phase165_r52_r9_shared_math.py.r52_r16_r2_backup"
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(updated, encoding="utf-8")
    print("R16-R2: nullable migration record guard installed")
elif source.count(new) == 1:
    print("R16-R2: already installed")
else:
    raise SystemExit("Unexpected R16 migration merge function; no changes made")
