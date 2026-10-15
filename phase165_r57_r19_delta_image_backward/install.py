"""Fail-closed R57-R19 installer. Only one existing function is replaced."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def _replace_function(source: str, name: str, previous: str, desired: str) -> tuple[str, bool]:
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("missing or duplicated " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    existing = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    if existing == desired.strip():
        return source, False
    if existing != previous.strip():
        raise RuntimeError("Unexpected previous shared provider; no changes applied")
    updated = "".join(lines[:node.lineno - 1]) + desired.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated, True


def install(root: Path, package: Path) -> str:
    shared = root / "phase165_r52_r9_shared_math.py"
    helper = root / "phase165_r57_r19_delta_image_backward.py"
    previous = root / "phase165_r57_r12_ordered_internal_transport" / "shared_expansion_provider.py.txt"
    if not shared.is_file() or not previous.is_file():
        raise RuntimeError("R57-R12 shared provider is required")
    desired_source = (package / "shared_expansion_provider.py.txt").read_text(encoding="utf8")
    original = shared.read_text(encoding="utf8")
    updated, changed = _replace_function(
        original, "shared_expansion_provider",
        previous.read_text(encoding="utf8"), desired_source,
    )
    new_helper = (package / helper.name).read_text(encoding="utf8")
    ast.parse(new_helper)
    if helper.exists() and helper.read_text(encoding="utf8") != new_helper:
        raise RuntimeError("conflicting R57-R19 module; no changes applied")
    if changed:
        backup = shared.with_name(shared.name + ".r57_r19_before.bak")
        if not backup.exists():
            shutil.copy2(shared, backup)
        shared.write_text(updated, encoding="utf8")
    if not helper.exists():
        helper.write_text(new_helper, encoding="utf8")
    return "INSTALLED" if changed else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R19:", install(package.parent, package))
    print("Reversed existing Delta image rule from screened typed References; no GIVEN synthesized")
    print("Full pytest NOT run")
