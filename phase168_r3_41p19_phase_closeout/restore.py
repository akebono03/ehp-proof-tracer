"""Restore one file only if it matches the installed or original checksum."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    manifest_path = OUTPUT / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("installation manifest missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    target = ROOT / manifest["target"]
    backup = (OUTPUT / manifest["backup"]).read_bytes()
    if digest(backup) != manifest["before_sha256"]:
        raise RuntimeError("backup checksum mismatch; refusing restore")
    if digest(target.read_bytes()) not in (
        manifest["before_sha256"], manifest["after_sha256"],
    ):
        raise RuntimeError("target was edited since installation; refusing overwrite")
    target.write_bytes(backup)
    if target.read_bytes() != backup:
        raise RuntimeError("restore verification failed")
    manifest_path.replace(OUTPUT / "manifest.restored.json")
    print("RESTORED", target)


if __name__ == "__main__":
    main()
