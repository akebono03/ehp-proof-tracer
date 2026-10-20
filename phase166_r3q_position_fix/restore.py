"""Restore the production module from the backup made in this run."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
bundle = Path(__file__).resolve().parent
record = bundle / "last_backup.txt"
if not record.exists():
    raise SystemExit("No backup was recorded; restore not attempted")
backup = Path(record.read_text(encoding="utf-8").strip())
if not backup.is_file() or backup.name != "phase166_r3p_position_binding.py":
    raise SystemExit("Invalid backup path; restore not attempted")
shutil.copy2(backup, root / backup.name)
print("RESTORED:", backup)
