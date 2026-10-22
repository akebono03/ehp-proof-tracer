"""Guarded installation: only the Phase 168 R2 shared-provider insertion."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MODULE = ROOT / "phase168_r2_toda52_transport.py"
SOURCE = PACKAGE / MODULE.name
ANCHOR = "        options.extend(expand_finite_cyclic_relation(goal))"
INSERT = (
    "        from phase168_r2_toda52_transport import expand_toda52_finite_cyclic_goal\n"
    "        options.extend(expand_toda52_finite_cyclic_goal(goal, tuple(available)))\n"
)


def main() -> None:
    if not TARGET.exists() or not SOURCE.exists():
        raise SystemExit("Required source missing; nothing changed")
    before = TARGET.read_text(encoding="utf-8-sig")
    module = SOURCE.read_text(encoding="utf-8")
    ast.parse(before, filename=str(TARGET))
    ast.parse(module, filename=str(SOURCE))
    definition = next((node for node in ast.parse(before).body
                       if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                       and node.name == "shared_expansion_provider"), None)
    if definition is None:
        raise SystemExit("shared_expansion_provider not found")
    if "expand_toda52_finite_cyclic_goal" in before:
        print("ALREADY_INSTALLED: no files changed")
        return
    lines = before.splitlines(keepends=True)
    matches = [i for i in range(definition.lineno - 1, definition.end_lineno)
               if lines[i].rstrip("\r\n") == ANCHOR]
    if len(matches) != 1:
        raise SystemExit("Unexpected shared provider shape; nothing changed")
    i = matches[0]
    newline = "\r\n" if "\r\n" in before else "\n"
    lines.insert(i + 1, INSERT.replace("\n", newline))
    updated = "".join(lines)
    ast.parse(updated, filename=str(TARGET))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PACKAGE / "backup" / stamp
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(TARGET, backup / TARGET.name)
    if MODULE.exists():
        shutil.copy2(MODULE, backup / MODULE.name)
    shutil.copy2(SOURCE, MODULE)
    TARGET.write_text(updated, encoding="utf-8", newline="")
    print("PATCHED:", TARGET)
    print("INSTALLED:", MODULE)
    print("BACKUP:", backup)
    print("CHANGED_FUNCTION: phase165_r52_r9_shared_math.shared_expansion_provider")
    updated_tree = ast.parse(updated)
    full_function = next(node for node in updated_tree.body
                         if isinstance(node, ast.FunctionDef)
                         and node.name == "shared_expansion_provider")
    complete = "".join(updated.splitlines(keepends=True)[full_function.lineno - 1:full_function.end_lineno])
    full_path = PACKAGE / "changed_function_full.py.txt"
    full_path.write_text(complete, encoding="utf-8")
    print("FULL_FUNCTION:", full_path)
    print("NEW_MODULE: phase168_r2_toda52_transport.py")


if __name__ == "__main__":
    main()
