"""R57-R16 targeted fail-closed installation, no unrelated refactoring."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def replace_function(source: str, name: str, expected: str, desired: str) -> tuple[str, bool]:
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("expected one function: " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    current = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    if current == desired.strip():
        return source, False
    if current != expected.strip():
        raise RuntimeError("unexpected R57-R15 predecessor; refusing to overwrite " + name)
    updated = "".join(lines[:node.lineno - 1]) + desired.rstrip("\n") + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated, True


def install(root: Path, package: Path) -> str:
    target = root / "phase165_r55_nk_only_goal.py"
    predecessor = root / "phase165_r57_r15_ordinary_recursive_connection" / "search_group_from_registered_goal.py.txt"
    if not target.is_file() or not predecessor.is_file():
        raise RuntimeError("R57-R15 and R55 must be installed first")
    current = target.read_text(encoding="utf8")
    desired = (package / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")
    old = predecessor.read_text(encoding="utf8")
    updated, changed = replace_function(current, "search_group_from_registered_goal", old, desired)
    module = package / "phase165_r57_r16_web_proof_order.py"
    if not module.is_file():
        raise RuntimeError("missing order-policy module")
    ast.parse(module.read_text(encoding="utf8"))
    destination = root / module.name
    if destination.is_file() and destination.read_bytes() != module.read_bytes():
        raise RuntimeError("unexpected existing proof order module")
    if changed:
        backup = target.with_name(target.name + ".r57_r16_before.bak")
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_text(updated, encoding="utf8")
    if not destination.exists():
        shutil.copy2(module, destination)
    return "INSTALLED" if changed else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R16:", install(package.parent, package))
    print("Explicit reviewed proof order supplied to normal n,k search; no ProofStep persisted")
    print("Full pytest NOT run")
