"""Guarded Phase 169 R3S1 function replacement; no general renderer changes."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil
import subprocess

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
TARGET = REPO / "phase168_r3_37c_reference_projection.py"
BASELINE = PACKAGE / "baseline_function.py"
OLD_R3S = PACKAGE / "r3s_failed_function.py"
REPLACEMENT = PACKAGE / "full_functions" / "project_reference_bodies_FULL.py"
OUTPUT = PACKAGE / "output"


def function_node(source: str) -> ast.FunctionDef:
    found = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef)
             and node.name == "project_reference_bodies"]
    if len(found) != 1:
        raise RuntimeError("expected one project_reference_bodies()")
    return found[0]


def same_function(left: str, right: str) -> bool:
    return (ast.dump(function_node(left), include_attributes=False)
            == ast.dump(function_node(right), include_attributes=False))


def apply() -> None:
    if not (REPO / ".git").is_dir():
        raise RuntimeError("extract this package inside the Git repository")
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    print("R3S1_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("R3S1 requires develop branch")
    OUTPUT.mkdir(exist_ok=True)
    current = TARGET.read_text(encoding="utf-8-sig")
    baseline = BASELINE.read_text(encoding="utf-8")
    old_r3s = OLD_R3S.read_text(encoding="utf-8")
    replacement = REPLACEMENT.read_text(encoding="utf-8")
    if same_function(current, replacement):
        print("R3S1_ALREADY_INSTALLED=True")
        return
    if not (same_function(current, baseline) or same_function(current, old_r3s)):
        raise RuntimeError("R3S1 guard mismatch: unexpected existing reference function")
    node = function_node(current)
    source_lines = current.splitlines(keepends=True)
    start, end = node.lineno - 1, node.end_lineno
    patch = replacement
    if end < len(source_lines) and source_lines[end].strip():
        patch += "\n"
    updated = "".join(source_lines[:start]) + patch + "".join(source_lines[end:])
    ast.parse(updated)
    backup = OUTPUT / (TARGET.name + ".before")
    if backup.exists():
        if backup.read_text(encoding="utf-8-sig") != current:
            raise RuntimeError("backup exists but no longer matches input")
    else:
        shutil.copy2(TARGET, backup)
    (OUTPUT / TARGET.name).write_text(updated, encoding="utf-8")
    TARGET.write_text(updated, encoding="utf-8")
    print("R3S1_PATCHED=" + TARGET.name)
    print("R3S1_FULL_FUNCTION=" + str(REPLACEMENT))
    print("R3S1_FULL_FILE=" + str(OUTPUT / TARGET.name))
    print("R3S1_BACKUP=" + str(backup))


def restore() -> None:
    backup = OUTPUT / (TARGET.name + ".before")
    if not backup.is_file():
        raise RuntimeError("no R3S1 backup exists")
    shutil.copy2(backup, TARGET)
    print("R3S1_RESTORED=" + TARGET.name)


if __name__ == "__main__":
    apply()
