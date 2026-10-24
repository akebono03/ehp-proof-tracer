"""Safe restoration for the single edited Typed Projection file."""
from __future__ import annotations
import json
from pathlib import Path
from .patch import BACKUP, OUTPUT, TARGET, sha256


def restore() -> None:
    record = OUTPUT / "post_patch.json"
    if not BACKUP.is_file() or not record.is_file():
        raise FileNotFoundError("Missing backup or post-patch manifest")
    report = json.loads(record.read_text(encoding="utf-8"))
    if sha256(BACKUP.read_bytes()) != report["before_sha256"]:
        raise ValueError("Backup checksum is invalid")
    if not TARGET.is_file() or sha256(TARGET.read_bytes()) != report["after_sha256"]:
        raise ValueError("Target has changed after patch; refusing unsafe restore")
    staging = TARGET.with_name(TARGET.name + ".r341p6.restore.tmp")
    try:
        staging.write_bytes(BACKUP.read_bytes())
        staging.replace(TARGET)
    finally:
        if staging.exists():
            staging.unlink()
    print("RESTORED", TARGET)


if __name__ == "__main__":
    restore()
