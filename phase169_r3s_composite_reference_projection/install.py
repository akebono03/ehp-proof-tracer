"""Guarded, function-only Phase 169 R3S installer."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
TARGET = REPO / "phase168_r3_37c_reference_projection.py"
BASELINE = PACKAGE / "baseline_function.py"
REPLACEMENT = PACKAGE / "full_functions" / "project_reference_bodies_FULL.py"
OUTPUT = PACKAGE / "output"


def _function_node(source: str) -> ast.FunctionDef:
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef)
             and node.name == "project_reference_bodies"]
    if len(nodes) != 1:
        raise RuntimeError("exactly one project_reference_bodies function required")
    return nodes[0]


def _same_ast(a: str, b: str) -> bool:
    return ast.dump(_function_node(a), include_attributes=False) == ast.dump(
        _function_node(b), include_attributes=False)


def apply() -> None:
    if not (REPO / ".git").is_dir():
        raise RuntimeError("run from extracted package inside repository")
    OUTPUT.mkdir(exist_ok=True)
    original = TARGET.read_text(encoding="utf-8-sig")
    expected = BASELINE.read_text(encoding="utf-8")
    replacement = REPLACEMENT.read_text(encoding="utf-8")
    node = _function_node(original)
    ast.parse(replacement)
    if _same_ast(original, replacement):
        print("R3S_ALREADY_INSTALLED=True")
        return
    if not _same_ast(original, expected):
        raise RuntimeError("reference projection function differs from audited GitHub baseline; no changes made")
    lines = original.splitlines(keepends=True)
    start = node.lineno - 1
    end = node.end_lineno
    if end < len(lines) and lines[end].strip():
        replacement += "\n"
    patched = "".join(lines[:start]) + replacement + "".join(lines[end:])
    ast.parse(patched)
    backup = OUTPUT / (TARGET.name + ".before")
    if backup.exists():
        if backup.read_text(encoding="utf-8-sig") != original:
            raise RuntimeError("backup differs from current baseline; refusing to overwrite it")
    else:
        shutil.copy2(TARGET, backup)
    (OUTPUT / TARGET.name).write_text(patched, encoding="utf-8")
    TARGET.write_text(patched, encoding="utf-8")
    print("R3S_PATCHED=" + TARGET.name)
    print("R3S_FULL_FILE=" + str(OUTPUT / TARGET.name))
    print("R3S_BACKUP=" + str(backup))


def restore() -> None:
    backup = OUTPUT / (TARGET.name + ".before")
    if not backup.exists():
        raise RuntimeError("missing backup")
    shutil.copy2(backup, TARGET)
    print("R3S_RESTORED=" + TARGET.name)


if __name__ == "__main__":
    apply()
