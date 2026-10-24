"""Restore the original R3-29 focused test, without overwriting later edits."""
from __future__ import annotations

import json
import os
from pathlib import Path

from .apply_test_fix import BACKUP_DIR, PROJECT, TARGET, sha256


def restore_legacy_test(project: Path = PROJECT, backup_dir: Path = BACKUP_DIR) -> dict[str, str]:
    """Restore only when the current file still matches our patch's hash."""
    project = Path(project)
    backup_dir = Path(backup_dir)
    path = project / TARGET
    backup = backup_dir / "r3_29_test_original.bin"
    state = backup_dir / "r3_29_test_state.json"
    metadata = json.loads(state.read_text(encoding="utf-8"))
    if metadata["target"] != TARGET.as_posix():
        raise ValueError("Backup target mismatch")
    original = backup.read_bytes()
    current = path.read_bytes()
    if sha256(original) != metadata["original_sha256"]:
        raise ValueError("Backup content mismatch")
    if sha256(current) == metadata["original_sha256"]:
        return {"status": "already_restored", "file": str(path)}
    if sha256(current) != metadata["patched_sha256"]:
        raise ValueError("Test has later edits; refusing to overwrite")
    temp = path.with_name(path.name + ".r341p2_restore.tmp")
    try:
        temp.write_bytes(original)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
    return {"status": "restored", "file": str(path)}


def main() -> int:
    try:
        outcome = restore_legacy_test()
    except Exception as exc:
        print("R3-41P2 RESTORE_ERROR", f"{type(exc).__name__}: {exc}")
        return 1
    print("R3-41P2 TEST_RESTORE", outcome["status"], outcome["file"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
