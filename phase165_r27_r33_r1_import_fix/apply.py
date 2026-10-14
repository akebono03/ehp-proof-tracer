"""R27-R33-R1: restore exact imports needed by the migrated Web group entry."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
FILE = "web_group_proof.py"
REQUIRED = {
    "toda_group_query": ("TodaGroupQuery",),
    "toda_group_query_semantics": (
        "TodaGroupQueryDomainKind",
        "classify_toda_group_query_domain",
    ),
}


def patch(source: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "build_standard_web_group_proof_view"
    ]
    if len(functions) != 1:
        raise RuntimeError("Expected exactly one standard Web group-proof entry")
    used = {
        node.id for node in ast.walk(functions[0])
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    if "search_group_structure_automatically" not in used:
        raise RuntimeError("R27-R33 typed search is not installed: refusing import-only repair")

    needed = []
    for module, names in REQUIRED.items():
        for name in names:
            if name not in used:
                continue
            matching = [
                node for node in tree.body
                if isinstance(node, ast.ImportFrom)
                and node.module == module
                and any(alias.name == name and alias.asname is None for alias in node.names)
            ]
            if not matching:
                needed.append(f"from {module} import {name}\n")
    if not needed:
        return source, False

    # Add imports after the initial import group, but never inside a function.
    lines = source.splitlines(keepends=True)
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    if imports:
        pos = max(node.end_lineno for node in imports)
    else:
        pos = 0
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str):
            pos = tree.body[0].end_lineno
    lines[pos:pos] = ["\n", *needed]
    updated = "".join(lines)
    ast.parse(updated)
    return updated, True


def apply(root: Path = ROOT) -> None:
    target = root / FILE
    original = target.read_text(encoding="utf-8-sig")
    updated, changed = patch(original)
    if not changed:
        print("R27-R33-R1: required Web Group Proof imports already present")
        return
    backup = root / "phase165_r27_r33_r1_web_group_proof_backup.py.bak"
    if backup.exists() and backup.read_text(encoding="utf-8") != original:
        raise RuntimeError("R33-R1 backup collision: refusing overwrite")
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(updated, encoding="utf-8")
    print("R27-R33-R1 installed: missing typed Group Query imports restored")


if __name__ == "__main__":
    apply()
