"""Minimal idempotent installer: preserve the locally patched shared module."""
from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
PACKAGE = Path(__file__).resolve().parent
SOURCE = PACKAGE / "phase165_r52_r23_existing_rule_adapter.py"
MARKER = "expand_existing_pi43_rules,"
IMPORT = "from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules\n"


def install() -> str:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    original = TARGET.read_text(encoding="utf-8")
    if MARKER in original:
        return "R23 adapter already installed"
    anchor = "            expand_diagonal_suspension,"
    if original.count(anchor) != 1:
        raise RuntimeError("Expected common-provider anchor not unique; no changes made")
    import_anchor = "from phase165_r3_recursive_search import GoalExpansion\n"
    if original.count(import_anchor) != 1:
        raise RuntimeError("Expected import anchor not unique; no changes made")
    changed = original.replace(import_anchor, IMPORT + import_anchor, 1)
    changed = changed.replace(anchor, anchor + "\n            " + MARKER, 1)
    compile(changed, str(TARGET), "exec")
    compile(SOURCE.read_text(encoding="utf-8"), str(SOURCE), "exec")
    backup = TARGET.with_name("phase165_r52_r9_shared_math.phase165_r52_r23_backup.py")
    if backup.exists():
        raise RuntimeError("R23 backup already exists but adapter is absent; no changes made")
    shutil.copy2(TARGET, backup)
    shutil.copy2(SOURCE, ROOT / SOURCE.name)
    TARGET.write_text(changed, encoding="utf-8")
    return "R23 existing-rule reverse adapter installed (backup preserved)"


if __name__ == "__main__":
    print(install())
