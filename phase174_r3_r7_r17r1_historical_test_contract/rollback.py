"""Restore only the exact reviewed R17 formatter patch after a failed R17R1 run."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    EXPECTED_BLOB, TARGET, expected_patched_bytes, matches_git_blob,
    normalize_and_style,
)

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r17" / "web_group_proof_common.original.py"


def main() -> int:
    if not BACKUP.is_file():
        print("PHASE174_R3R7R17R1_FORMATTER_ROLLBACK=NO_BACKUP")
        return 0
    original = BACKUP.read_bytes()
    if not matches_git_blob(original, EXPECTED_BLOB):
        raise RuntimeError("R17 formatter backup not equal to reviewed source")
    live = ROOT / TARGET
    current = live.read_bytes()
    text, _ = normalize_and_style(current)
    old_text, _ = normalize_and_style(original)
    patched_text, _ = normalize_and_style(expected_patched_bytes(original))
    if text == old_text:
        print("PHASE174_R3R7R17R1_FORMATTER_ROLLBACK=ALREADY_ORIGINAL")
        return 0
    if text != patched_text:
        raise RuntimeError("Refusing to overwrite an unreviewed formatter")
    live.write_bytes(original)
    print("PHASE174_R3R7R17R1_FORMATTER_ROLLBACK=RESTORED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
