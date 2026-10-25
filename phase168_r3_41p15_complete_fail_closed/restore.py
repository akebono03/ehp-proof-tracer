"""Restore the exact two reviewed files from their checked P15 backups."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def main() -> None:
    manifest = OUTPUT / "manifest.json"
    if not manifest.is_file():
        raise FileNotFoundError("R3-41P15 manifest is missing")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    changes = data["changed"]
    for relative, record in changes.items():
        target = ROOT / relative
        backup = OUTPUT / record["backup"]
        before = backup.read_bytes()
        current = target.read_bytes()
        if hashlib.sha256(before).hexdigest() != record["before_sha256"]:
            raise RuntimeError(f"backup digest mismatch: {relative}")
        if hashlib.sha256(current).hexdigest() not in (
            record["before_sha256"], record["after_sha256"],
        ):
            raise RuntimeError(f"source changed after installation: {relative}")
    for relative, record in changes.items():
        target = ROOT / relative
        before = (OUTPUT / record["backup"]).read_bytes()
        target.write_bytes(before)
        if target.read_bytes() != before:
            raise RuntimeError(f"restore verification failed: {relative}")
        print("RESTORED", target)
    manifest.rename(OUTPUT / "manifest.restored.json")


if __name__ == "__main__":
    main()
