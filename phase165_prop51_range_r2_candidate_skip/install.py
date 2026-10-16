from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r57_r8_eta_specialization.py"
BACKUP = ROOT / "phase165_r57_r8_eta_specialization.py.prop51_range_r2_before.bak"


def install() -> dict[str, object]:
    text = TARGET.read_text(encoding="utf-8")
    original = text
    ast.parse(text)
    tree = ast.parse(text)
    intended = {"specialized_eta_group_goal_candidates", "expand_registered_eta_specialization"}
    seen = set()
    lines = text.splitlines(keepends=True)
    replacements = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name not in intended:
            continue
        seen.add(node.name)
        candidates = [item for item in ast.walk(node) if isinstance(item, ast.Compare)
                      and len(item.ops) == 1 and isinstance(item.ops[0], ast.Lt)
                      and len(item.comparators) == 1 and isinstance(item.comparators[0], ast.Constant)
                      and item.comparators[0].value in (3, 4)
                      and isinstance(item.left, ast.Name) and item.left.id == "n"]
        if len(candidates) != 1:
            raise RuntimeError(f"unexpected range check in {node.name}: {len(candidates)}")
        comparison = candidates[0]
        old_line = lines[comparison.lineno - 1]
        old_segment = old_line[comparison.col_offset:comparison.end_col_offset]
        if old_segment not in ("n < 3", "n < 4"):
            raise RuntimeError(f"unexpected source in {node.name}: {old_segment!r}")
        if old_segment == "n < 3":
            new_line = old_line[:comparison.col_offset] + "n < 4" + old_line[comparison.end_col_offset:]
            replacements.append((comparison.lineno - 1, new_line))
    if seen != intended:
        raise RuntimeError(f"missing expected functions: {sorted(intended - seen)}")
    for i, replacement in replacements:
        lines[i] = replacement
    updated = "".join(lines)
    ast.parse(updated)
    if updated != original:
        if not BACKUP.exists():
            shutil.copy2(TARGET, BACKUP)
        TARGET.write_text(updated, encoding="utf-8")
    return {"status": "INSTALLED" if updated != original else "ALREADY_INSTALLED",
            "modified_file": TARGET.name, "backup": str(BACKUP) if BACKUP.exists() else None,
            "full_pytest_run": False}


if __name__ == "__main__":
    print(json.dumps(install(), ensure_ascii=False))
