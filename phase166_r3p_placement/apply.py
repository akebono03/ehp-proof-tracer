from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SHARED = ROOT / "phase165_r52_r9_shared_math.py"
COMPARE = ROOT / "phase166_r3c_publication_order.py"
TARGET = ROOT / "phase166_r3p_position_binding.py"


def main() -> None:
    original = SHARED.read_text(encoding="utf-8")
    tree = ast.parse(original)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build_shared_typed_bridge"]
    if len(matches) != 1:
        raise RuntimeError("expected one build_shared_typed_bridge")
    node = matches[0]
    lines = original.splitlines(keepends=True)
    function = "".join(lines[node.lineno - 1:node.end_lineno])
    old = "    ordered, _order_report = connect_all_reference_orders(joined)\n    return ordered"
    new = ("    ordered, _order_report = connect_all_reference_orders(joined)\n"
           "    from phase166_r3p_position_binding import place_r3p_reference_positions\n"
           "    return place_r3p_reference_positions(ordered)")
    if old in function and new not in function:
        function = function.replace(old, new)
    elif new in function:
        pass
    else:
        raise RuntimeError("R3-L/R3-N shared bridge tail did not match: no files changed")
    updated = "".join(lines[:node.lineno - 1]) + function + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    comparison = (PACKAGE / "phase166_r3p_order_comparison.py").read_text(encoding="utf-8")
    ast.parse(comparison)
    registration = (PACKAGE / "phase166_r3p_position_binding.py").read_text(encoding="utf-8")
    ast.parse(registration)
    if not COMPARE.exists():
        raise RuntimeError("expected existing order comparison module")
    backup = ROOT / "phase166_r3p_backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup.mkdir(parents=True, exist_ok=True)
    for filename in (SHARED, COMPARE):
        shutil.copy2(filename, backup / filename.name)
    SHARED.write_text(updated, encoding="utf-8")
    COMPARE.write_text(comparison, encoding="utf-8")
    shutil.copy2(PACKAGE / "phase166_r3p_position_binding.py", TARGET)
    print("PATCHED:", SHARED.name, COMPARE.name, TARGET.name)
    print("BACKUP:", backup)
    print("FULL MODIFIED FUNCTION: build_shared_typed_bridge")
    print(function)
    print("FULL MODIFIED FUNCTION: precedes_citing_assertion")
    print(comparison)
    print("FULL NEW FUNCTION: place_r3p_reference_positions")
    print(registration)


if __name__ == "__main__":
    main()
