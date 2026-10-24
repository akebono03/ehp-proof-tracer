"""Restore only Phase 168 R3-41P3 modified files from saved backups."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "backups"


def main() -> int:
    manifest = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        filename = entry["name"]
        if filename not in {
            "phase168_r3_5_model_renderer.py",
            "phase168_r3_27_typed_statement_projection.py",
        }:
            raise ValueError("Unexpected backup target: " + filename)
        original = (BACKUP / filename).read_bytes()
        if hashlib.sha256(original).hexdigest() != entry["sha256_before"]:
            raise ValueError("Backup content checksum mismatch: " + filename)
        current = (PROJECT / filename).read_bytes()
        if hashlib.sha256(current).hexdigest() != entry["sha256_after"]:
            raise ValueError("Source changed after this patch; refusing overwrite: " + filename)
        (PROJECT / filename).write_bytes(original)
        print("RESTORED", PROJECT / filename)
    print("R3-41P3_SOURCE_RESTORED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
