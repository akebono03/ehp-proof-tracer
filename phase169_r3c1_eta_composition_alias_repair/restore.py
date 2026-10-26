"""Restore a single R3C1 patch only while the file is unchanged since patch."""
from __future__ import annotations

import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase165_r12_r21_eta_generator_chain.py"
REPLACEMENT = PACKAGE / "full_files" / TARGET.name
BACKUP = PACKAGE / "output" / (TARGET.name + ".before")


def restore() -> int:
    if not BACKUP.is_file() or not REPLACEMENT.is_file():
        print("RESTORE_SKIPPED: no reviewed backup or replacement available")
        return 1
    normalized = lambda path: path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if normalized(TARGET) != normalized(REPLACEMENT):
        print("RESTORE_SKIPPED: target has changed since R3C1 patch")
        return 2
    shutil.copy2(BACKUP, TARGET)
    print("RESTORED:", TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(restore())
