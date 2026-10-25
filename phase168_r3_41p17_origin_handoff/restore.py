"""Verify and restore byte-exact application files from the P17 backup."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    manifest_path = OUTPUT / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("P17 installation manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    capture = ROOT / manifest["new_file"]
    changes = manifest["changed"]
    for relative, record in changes.items():
        target = ROOT / relative
        backup = (OUTPUT / record["backup"]).read_bytes()
        if sha(backup) != record["before_sha256"]:
            raise RuntimeError("P17 backup checksum mismatch: " + relative)
        if sha(target.read_bytes()) not in (record["before_sha256"], record["after_sha256"]):
            raise RuntimeError("P17 file modified after installation: " + relative)
    if capture.exists() and sha(capture.read_bytes()) != manifest["new_sha256"]:
        raise RuntimeError("P17 capture module modified after installation; refusing delete")
    for relative, record in changes.items():
        target = ROOT / relative
        backup = (OUTPUT / record["backup"]).read_bytes()
        target.write_bytes(backup)
        if target.read_bytes() != backup:
            raise RuntimeError("P17 restore verification failed: " + relative)
        print("RESTORED", target)
    if capture.exists():
        capture.unlink()
    # Repeated safe restore cycles may already have a restored manifest.
    # Replacing its historical marker is safe only after all checksum checks.
    manifest_path.replace(OUTPUT / "manifest.restored.json")
    print("REMOVED", capture)

if __name__ == "__main__":
    main()
