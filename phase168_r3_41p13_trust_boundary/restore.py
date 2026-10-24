"""Restore the sole changed application file byte-for-byte."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def main() -> None:
    backup = OUTPUT / "web_group_proof.py.before"
    manifest = OUTPUT / "manifest.json"
    target = ROOT / "web_group_proof.py"
    if not backup.is_file() or not manifest.is_file():
        raise FileNotFoundError("Missing R3-41P13 backup or manifest")
    meta = json.loads(manifest.read_text(encoding="utf-8"))
    before = backup.read_bytes()
    if hashlib.sha256(before).hexdigest() != meta["before_sha256"]:
        raise RuntimeError("Backup digest mismatch")
    installed = target.read_bytes()
    if hashlib.sha256(installed).hexdigest() != meta["after_sha256"]:
        raise RuntimeError("Current source changed since installation; refusing overwrite")
    target.write_bytes(before)
    if target.read_bytes() != before:
        raise RuntimeError("Restore failed to produce the original file")
    print("RESTORED", target)


if __name__ == "__main__":
    main()
