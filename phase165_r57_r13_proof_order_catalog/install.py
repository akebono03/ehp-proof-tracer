"""Fail-closed R57-R13 installer for the local R57-R12 baseline."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def install(root: Path, package: Path) -> str:
    destination = root / "phase165_r52_r9_shared_math.py"
    helper = root / "phase165_r57_r13_proof_order_catalog.py"
    supplied = (package / helper.name).read_bytes()
    if helper.exists() and helper.read_bytes() != supplied:
        raise RuntimeError("R57-R13 catalog module differs; abort")
    current = destination.read_text(encoding="utf-8")
    nodes = [item for item in ast.parse(current).body if isinstance(item, ast.FunctionDef)
             and item.name == "search_shared_group_goal"]
    if len(nodes) != 1:
        raise RuntimeError("shared search entry must occur exactly once")
    node = nodes[0]
    lines = current.splitlines(keepends=True)
    body = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    expected = (package / "search_shared_group_goal.py.txt").read_text(encoding="utf-8").strip()
    if body == expected:
        if not helper.exists():
            shutil.copy2(package / helper.name, helper)
        return "ALREADY_INSTALLED"
    if "ordered_completed_proofs" not in body or "validate_prior_internal_proofs" not in body:
        raise RuntimeError("R57-R12 ordered-proof prerequisite is missing")
    if "proof_order_catalog" in body:
        raise RuntimeError("unexpected order-catalog integration; abort")
    if "prior = validate_prior_internal_proofs(" not in body:
        raise RuntimeError("unrecognized R57-R12 search implementation")
    replacement = "".join(lines[:node.lineno - 1]) + expected + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(replacement)
    backup = destination.with_name(destination.name + ".r57_r13_before.bak")
    if not backup.exists():
        shutil.copy2(destination, backup)
    if not helper.exists():
        shutil.copy2(package / helper.name, helper)
    destination.write_text(replacement, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R13:", install(package.parent, package))
    print("Registered prior proofs selected by catalog order; no GIVEN synthesized; full pytest NOT run")
