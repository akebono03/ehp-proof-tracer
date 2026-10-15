"""Guarded replacement of the remaining standard Web proof entry search path."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "web_group_proof.py"
SOURCE = Path(__file__).resolve().parent / "replacement_function.py.txt"


def install() -> None:
    if not TARGET.is_file():
        raise RuntimeError(f"target not found: {TARGET}")
    for filename, marker in (
        ("phase165_r55_nk_only_goal.py", "search_group_from_registered_goal"),
        ("phase165_r56_presentation_adapter.py", "render_toda_group_proof_narrative_markdown"),
        ("phase165_r52_r3_web_adapter.py", "build_partial_web_group_proof_view"),
    ):
        file = ROOT / filename
        if not file.is_file() or marker not in file.read_text(encoding="utf-8"):
            raise RuntimeError(f"required installed implementation missing: {file}")
    current = TARGET.read_text(encoding="utf-8")
    replacement = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(current)
    fn = [f for f in tree.body if isinstance(f, ast.FunctionDef) and f.name == "build_standard_web_group_proof_view"]
    if len(fn) != 1:
        raise RuntimeError("expected exactly one standard Web group proof function")
    node = fn[0]
    lines = current.splitlines(keepends=True)
    previous = "".join(lines[node.lineno - 1: node.end_lineno])
    if "search_group_from_registered_goal" in previous:
        print("R57-R1: standard Web group-proof entry already consolidated")
        return
    if "search_group_structure_automatically" not in previous:
        raise RuntimeError("unrecognized baseline; no modification")
    updated = "".join(lines[:node.lineno-1]) + replacement + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    backup = ROOT / "web_group_proof.py.phase165_r57_r1_backup"
    if not backup.exists():
        shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding="utf-8")
    print("R57-R1: standard Web group proof now uses registered n,k selection")
    print("Original file backup:", backup)


if __name__ == "__main__":
    install()
