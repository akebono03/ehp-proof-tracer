"""Guarded full-file replacement at the reviewed Phase 169 R3A repository state."""
from __future__ import annotations

import ast
import hashlib
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase165_r12_r24_web_search_connection.py"
BASELINE = PACKAGE / "baseline" / TARGET.name
REPLACEMENT = PACKAGE / "full_files" / TARGET.name
BACKUP = PACKAGE / "output" / (TARGET.name + ".before")


def _normalized(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def apply() -> int:
    original = _normalized(TARGET)
    baseline = _normalized(BASELINE)
    updated = _normalized(REPLACEMENT)
    if original == updated:
        print("ALREADY_APPLIED: " + str(TARGET))
        return 0
    if original != baseline:
        print("REFUSED: production source differs from reviewed baseline. No files changed.")
        print("ACTUAL_SHA256=" + hashlib.sha256(original.encode()).hexdigest())
        print("EXPECTED_SHA256=" + hashlib.sha256(baseline.encode()).hexdigest())
        return 2
    ast.parse(baseline, filename=str(BASELINE))
    ast.parse(updated, filename=str(REPLACEMENT))
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and _normalized(BACKUP) != baseline:
        print("REFUSED: previous backup is not the reviewed baseline.")
        return 3
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(updated, encoding="utf-8", newline="\n")
    if _normalized(TARGET) != updated:
        print("REFUSED: output integrity mismatch; restoring original source.")
        shutil.copy2(BACKUP, TARGET)
        return 4
    print("PATCHED: " + str(TARGET))
    print("BACKUP: " + str(BACKUP))
    print("FULL_FILE: " + str(REPLACEMENT))
    print("FUNCTIONS: " + str(PACKAGE / "full_functions"))
    return 0


if __name__ == "__main__":
    raise SystemExit(apply())
