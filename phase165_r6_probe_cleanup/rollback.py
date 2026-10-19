from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python rollback.py PROJECT_ROOT SESSION_DIRECTORY", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    session = Path(sys.argv[2]).resolve()
    report = json.loads((session / "report.json").read_text(encoding="utf-8"))
    restored = 0
    for item in report["decisions"]:
        if item.get("result") != "BACKED_UP_AND_REMOVED":
            continue
        source = session / "backup" / item["path"]
        target = root / item["path"]
        if not source.is_file() or digest(source) != item["sha256"]:
            raise RuntimeError("Missing or modified backup: " + str(source))
        if target.exists():
            if digest(target) != item["sha256"]:
                raise RuntimeError("Conflicting current file: " + str(target))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        restored += 1
    print("Restored:", restored)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
