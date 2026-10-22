"""Replace the complete existing function by AST boundaries with a backup."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil


def main():
    package = Path(__file__).resolve().parent
    root = package.parent
    target = root / "phase166_r3t_goal_source_binding" / "goal_source.py"
    replacement = (package / "replacement_function.py").read_text(encoding="utf-8").rstrip("\n")
    source = target.read_text(encoding="utf-8")
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_same_group_structure"]
    if len(candidates) != 1:
        raise RuntimeError("Expected exactly one _same_group_structure function")
    lines = source.splitlines(keepends=True)
    node = candidates[0]
    current = "".join(lines[node.lineno - 1:node.end_lineno]).rstrip("\n")
    if current == replacement:
        print("ALREADY_APPLIED", target)
        return
    if 'a.generator == b.generator' not in current and 'same_registered_group_presentation' not in current:
        raise RuntimeError("Function body is not a recognized version; refusing replacement")
    backup_dir = root / "phase168_r2_8_3_backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(target, backup_dir / "goal_source.py")
    updated = "".join(lines[:node.lineno - 1]) + replacement + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    target.write_text(updated, encoding="utf-8")
    print("PATCHED", target)
    print("BACKUP", backup_dir / "goal_source.py")
    print("FULL_FUNCTION", package / "replacement_function.py")


if __name__ == "__main__":
    main()
