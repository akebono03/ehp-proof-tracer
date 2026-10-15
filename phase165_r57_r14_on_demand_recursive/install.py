"""Fail-closed, idempotent R57-R14 installer on top of R57-R13."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def install(root: Path, package: Path) -> str:
    destination = root / "phase165_r52_r9_shared_math.py"
    helper = root / "phase165_r57_r14_recursive_search.py"
    new_helper = (package / helper.name).read_bytes()
    if helper.exists() and helper.read_bytes() != new_helper:
        raise RuntimeError("conflicting recursive search helper")
    source = destination.read_text(encoding="utf-8")
    nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)
             and node.name == "search_shared_group_goal"]
    if len(nodes) != 1:
        raise RuntimeError("shared group search must have one definition")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    existing = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    expected = (package / "search_shared_group_goal.py.txt").read_text(encoding="utf-8").strip()
    if existing == expected:
        if not helper.exists():
            shutil.copy2(package / helper.name, helper)
        return "ALREADY_INSTALLED"
    prior = (package.parent / "phase165_r57_r13_proof_order_catalog" / "search_shared_group_goal.py.txt")
    if not prior.exists() or prior.read_text(encoding="utf-8").strip() != existing:
        raise RuntimeError("unexpected R57-R13 shared search; abort without changes")
    replacement = "".join(lines[:node.lineno - 1]) + expected + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(replacement)
    backup = destination.with_name(destination.name + ".r57_r14_before.bak")
    if not backup.exists():
        shutil.copy2(destination, backup)
    if not helper.exists():
        shutil.copy2(package / helper.name, helper)
    destination.write_text(replacement, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R14:", install(package.parent, package))
    print("On-demand earlier-proof recursion; no ProofStep persisted; full pytest NOT run")
