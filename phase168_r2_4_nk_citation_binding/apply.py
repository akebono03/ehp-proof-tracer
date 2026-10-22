from pathlib import Path
from datetime import datetime, timezone
import shutil

here = Path(__file__).resolve().parent
root = here.parent
target = root / "phase166_r3t_goal_source_binding" / "goal_source.py"
source = here / "goal_source.py"
if not target.exists():
    raise SystemExit("Target is missing: " + str(target))
original = target.read_text(encoding="utf-8")
if "def resolve_specialized_goal_citing_id(" not in original:
    raise SystemExit("Unexpected target: resolver missing")
backup = here / "backup" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
backup.mkdir(parents=True)
shutil.copy2(target, backup / target.name)
shutil.copy2(source, target)
print("PATCHED:", target)
print("BACKUP:", backup)
print("FULL_MODULE:", source)
