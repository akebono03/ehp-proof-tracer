"""Restore renderer cleanup from backup; keep current other project changes."""
from __future__ import annotations

from pathlib import Path
import shutil


def restore(project: Path) -> None:
    backup = project / ".renderer_single_implementation_backup"
    old = "toda_group_proof_generic_narrative_renderer.py"
    primary = "toda_group_proof_narrative_renderer.py"
    partial = "phase165_r52_partial_proof.py"
    for filename in (old, primary, partial):
        if not (backup / filename).is_file():
            raise FileNotFoundError("backup missing: " + filename)
    for filename in (old, primary, partial):
        shutil.copy2(backup / filename, project / filename)
    alias = project / "toda_group_proof_generic_narrative_renderer" / "__init__.py"
    if alias.exists():
        alias.unlink()
    alias_dir = alias.parent
    if alias_dir.is_dir():
        cache = alias_dir / "__pycache__"
        if cache.is_dir():
            shutil.rmtree(cache)
        alias_dir.rmdir()
    helper = project / "toda_group_proof_narrative_shared_components.py"
    if helper.exists():
        helper.unlink()
    print("Original renderer files restored from backup")


if __name__ == "__main__":
    restore(Path(__file__).resolve().parent.parent)
