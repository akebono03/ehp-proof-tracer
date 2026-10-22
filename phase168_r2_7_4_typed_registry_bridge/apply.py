"""Apply the minimal production integration after AST-based verification."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def apply(repo: Path, package: Path) -> None:
    target = repo / "phase165_r52_r9_shared_math.py"
    source = target.read_bytes()
    text = source.decode("utf-8")
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build_shared_typed_bridge"]
    if len(functions) != 1:
        raise RuntimeError("GUARD_MISMATCH: build_shared_typed_bridge not found uniquely")
    function = functions[0]
    assignments = [node for node in ast.walk(function)
                   if isinstance(node, ast.Assign)
                   and len(node.targets) == 1
                   and isinstance(node.targets[0], ast.Name)
                   and node.targets[0].id == "production"]
    if len(assignments) != 1:
        raise RuntimeError("GUARD_MISMATCH: production assignment not found uniquely")
    assignment = assignments[0]
    if not (isinstance(assignment.value, ast.Attribute)
            and assignment.value.attr == "bridge"
            and isinstance(assignment.value.value, ast.Call)
            and isinstance(assignment.value.value.func, ast.Name)
            and assignment.value.value.func.id == "discover_goal_search_inputs"):
        raise RuntimeError("GUARD_MISMATCH: production assignment changed")
    if "connect_explicit_literature_components" in ast.get_source_segment(text, function):
        print("ALREADY_PATCHED:", target)
    else:
        raw_lines = source.splitlines(keepends=True)
        after = raw_lines[assignment.end_lineno-1]
        newline = b"\r\n" if b"\r\n" in after else b"\n"
        indent = after[:len(after)-len(after.lstrip())]
        inserted = [
            indent + b"from phase168_r2_7_4_typed_registry_bridge.phase168_r2_7_4_literature_connection import (" + newline,
            indent + b"    connect_explicit_literature_components," + newline,
            indent + b")" + newline,
            indent + b"production = connect_explicit_literature_components(production)" + newline,
        ]
        updated = b"".join(raw_lines[:assignment.end_lineno] + inserted + raw_lines[assignment.end_lineno:])
        ast.parse(updated.decode("utf-8"))
        backup = package / "backup" / target.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
        target.write_bytes(updated)
        print("PATCHED:", target)
        print("BACKUP:", backup)
    updated_text = target.read_text(encoding="utf-8")
    parsed = ast.parse(updated_text)
    func = next(n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == "build_shared_typed_bridge")
    full = "\n".join(updated_text.splitlines()[func.lineno-1:func.end_lineno]) + "\n"
    output = package / "build_shared_typed_bridge_full.py"
    output.write_text(full, encoding="utf-8")
    print("FULL_FUNCTION:", output)


if __name__ == "__main__":
    repo = Path(__file__).resolve().parent.parent
    package = Path(__file__).resolve().parent
    apply(repo, package)
