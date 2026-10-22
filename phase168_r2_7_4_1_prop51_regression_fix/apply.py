"""Safely update only the R2-7(4) connector; retain shared Bridge patch."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def main() -> None:
    package = Path(__file__).resolve().parent
    root = package.parent
    target = root / "phase168_r2_7_4_typed_registry_bridge" / "phase168_r2_7_4_literature_connection.py"
    replacement = package / "phase168_r2_7_4_literature_connection.py"
    if not target.is_file():
        raise SystemExit("GUARD_MISMATCH: original R2-7(4) connector not installed")
    old = target.read_bytes()
    if b"def connect_explicit_literature_components(" not in old or b"register_prop51_prop53_literature_statements" not in old:
        raise SystemExit("GUARD_MISMATCH: unexpected original connector")
    if b"original_records.get(record.assertion_id, record)" in old:
        print("ALREADY_PATCHED:", target)
    else:
        backup = package / "backup" / target.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
        target.write_bytes(replacement.read_bytes())
        print("PATCHED:", target)
        print("BACKUP:", backup)
    tree = ast.parse(target.read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "connect_explicit_literature_components")
    lines = target.read_text(encoding="utf-8").splitlines()
    full = "\n".join(lines[function.lineno - 1:function.end_lineno]) + "\n"
    output = package / "connect_explicit_literature_components_full.py"
    output.write_text(full, encoding="utf-8")
    print("FULL_FUNCTION:", output)


if __name__ == "__main__":
    main()
