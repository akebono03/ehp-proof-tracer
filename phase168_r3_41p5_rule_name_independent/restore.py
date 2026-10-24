"""Restore exactly the original renderer backed up by R3-41P5."""
from __future__ import annotations

import json
from pathlib import Path

from .patch import BACKUP, OUTPUT, TARGET, EXPECTED_SHA256, digest


def restore() -> None:
    meta_path = OUTPUT / "post_patch.json"
    if not BACKUP.is_file() or not meta_path.is_file():
        raise FileNotFoundError("Patch backup or patch metadata missing")
    backup = BACKUP.read_bytes()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if digest(backup) != EXPECTED_SHA256:
        raise ValueError("Backup checksum mismatch: aborting restore")
    actual = digest(TARGET.read_bytes())
    if actual == EXPECTED_SHA256:
        print("ALREADY_RESTORED", TARGET)
        return
    if actual != meta["sha256_after"]:
        raise ValueError("Current file differs from patch output; refusing destructive restore")
    staging = TARGET.with_name(TARGET.name + ".r341p5.restore.tmp")
    try:
        staging.write_bytes(backup)
        staging.replace(TARGET)
    finally:
        if staging.exists():
            staging.unlink()
    print("RESTORED", TARGET)


if __name__ == "__main__":
    restore()
