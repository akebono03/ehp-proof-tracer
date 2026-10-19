from __future__ import annotations
import hashlib
import json
import shutil
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: rollback.py PROJECT_ROOT SESSION_DIRECTORY")
    root = Path(sys.argv[1]).resolve()
    session = Path(sys.argv[2]).resolve()
    report = json.loads((session / "report.json").read_text(encoding="utf-8"))
    for row in report["decisions"]:
        if row.get("result") != "REMOVED_AFTER_BACKUP":
            continue
        src = session / "backup" / row["path"]
        dest = root / row["path"]
        if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError("Backup invalid: " + row["path"])
        if dest.exists():
            if hashlib.sha256(dest.read_bytes()).hexdigest() != row["sha256"]:
                raise RuntimeError("Restore collision: " + row["path"])
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    print("Restored files from", session)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
