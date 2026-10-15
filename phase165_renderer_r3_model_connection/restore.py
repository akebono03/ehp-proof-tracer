"""Restore the two R3-modified files from the guarded backup."""
from __future__ import annotations

from pathlib import Path
import shutil


def restore(project: Path) -> None:
    backup = project / ".phase165_renderer_r3_backup"
    for name in (
        "toda_group_proof_narrative_renderer.py",
        "phase165_r52_partial_proof.py",
    ):
        original = backup / name
        if not original.is_file():
            raise FileNotFoundError(f"missing backup: {original}")
        shutil.copy2(original, project / name)


if __name__ == "__main__":
    restore(Path(__file__).resolve().parent.parent)
    print("R3 original renderer entry files restored")
