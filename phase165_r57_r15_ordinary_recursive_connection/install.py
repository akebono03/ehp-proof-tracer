"""R57-R15 fail-closed installer. Preserve all unrelated R55/R14 code."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def replace_function(source: str, name: str, expected: str, desired: str) -> tuple[str, bool]:
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError("expected exactly one function: " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    current = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    if current == desired.strip():
        return source, False
    if current != expected.strip():
        raise RuntimeError("unexpected predecessor function: " + name)
    result = "".join(lines[:node.lineno - 1]) + desired.rstrip("\n") + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(result)
    return result, True


def install(root: Path, package: Path) -> str:
    shared = root / "phase165_r52_r9_shared_math.py"
    selector = root / "phase165_r55_nk_only_goal.py"
    r14 = package.parent / "phase165_r57_r14_on_demand_recursive" / "search_shared_group_goal.py.txt"
    r55 = package.parent / "phase165_r55_nk_only_web" / "phase165_r55_nk_only_goal.py"
    if not r14.is_file() or not r55.is_file():
        raise RuntimeError("R57-R14 and R55 local source bundles are required")
    existing_shared = shared.read_text(encoding="utf8")
    existing_selector = selector.read_text(encoding="utf8")
    oldsel_tree = ast.parse(r55.read_text(encoding="utf8"))
    oldsel_node = next(n for n in oldsel_tree.body if isinstance(n, ast.FunctionDef) and n.name == "search_group_from_registered_goal")
    oldsel_lines = r55.read_text(encoding="utf8").splitlines(keepends=True)
    oldsel = "".join(oldsel_lines[oldsel_node.lineno - 1:oldsel_node.end_lineno])
    changes = []
    for path, current, name, expected, desired in (
        (shared, existing_shared, "search_shared_group_goal", r14.read_text(encoding="utf8"), (package / "search_shared_group_goal.py.txt").read_text(encoding="utf8")),
        (selector, existing_selector, "search_group_from_registered_goal", oldsel, (package / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")),
    ):
        updated, changed = replace_function(current, name, expected, desired)
        if changed:
            changes.append((path, updated))
    for path, updated in changes:
        backup = path.with_name(path.name + ".r57_r15_before.bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(updated, encoding="utf8")
    return "INSTALLED" if changes else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R15:", install(package.parent, package))
    print("Ordinary group search accepts on-demand proof-order catalog; no finished ProofStep persisted")
    print("Full pytest NOT run")
