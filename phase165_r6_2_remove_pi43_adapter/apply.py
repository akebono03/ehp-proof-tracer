"""Remove the obsolete pi4^3-only search adapter, fail closed on unexpected source."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import shutil

TARGET = "phase165_r52_r9_shared_math.py"
OLD_MODULE = "phase165_r52_r23_existing_rule_adapter"
OLD_FUNCTION = "expand_existing_pi43_rules"


def transform(source: str) -> str:
    """Remove exactly the legacy import and provider entry; retain everything else."""
    tree = ast.parse(source)
    imports = [node for node in tree.body if isinstance(node, ast.ImportFrom)
               and node.module == OLD_MODULE]
    if len(imports) != 1 or len(imports[0].names) != 1 or imports[0].names[0].name != OLD_FUNCTION:
        raise ValueError("expected unique pi43 adapter import missing/modified")
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "shared_expansion_provider"]
    if len(functions) != 1:
        raise ValueError("expected shared_expansion_provider missing/duplicated")
    names = [node for node in ast.walk(functions[0]) if isinstance(node, ast.Name)
             and node.id == OLD_FUNCTION]
    if len(names) != 1:
        raise ValueError("expected unique adapter use missing/modified")
    use = names[0]
    if not any(isinstance(node, (ast.Tuple, ast.List)) and use in node.elts
               for node in ast.walk(functions[0])):
        raise ValueError("adapter use is not direct provider tuple element")
    lines = source.splitlines(keepends=True)
    imp = imports[0]
    if imp.lineno != imp.end_lineno:
        raise ValueError("multiline import not supported")
    if lines[imp.lineno - 1].strip() != f"from {OLD_MODULE} import {OLD_FUNCTION}":
        raise ValueError("import text changed")
    if lines[use.lineno - 1].strip() != f"{OLD_FUNCTION},":
        raise ValueError("provider text changed")
    lines[use.lineno - 1] = ""
    lines[imp.lineno - 1] = ""
    result = "".join(lines)
    ast.parse(result)
    if OLD_MODULE in result or OLD_FUNCTION in result:
        raise ValueError("residual pi43 adapter reference in production module")
    return result


def install(root: Path) -> dict:
    """Backup and replace shared code, then quarantine the orphaned dedicated module."""
    target = root / TARGET
    obsolete = root / f"{OLD_MODULE}.py"
    if not target.is_file() or not obsolete.is_file():
        raise FileNotFoundError("required production files are missing; nothing changed")
    original = target.read_bytes()
    # Preserve local newline style through UTF-8 decoded text and splitlines.
    updated = transform(original.decode("utf-8"))
    backup = root / f"{TARGET}.r6_2_remove_pi43_before.bak"
    quarantine = root / f"{OLD_MODULE}.py.r6_2_removed.bak"
    if backup.exists() or quarantine.exists():
        raise FileExistsError("backups already exist; installation deliberately refuses overwrite")
    backup.write_bytes(original)
    try:
        target.write_bytes(updated.encode("utf-8"))
        shutil.move(str(obsolete), str(quarantine))
    except BaseException:
        target.write_bytes(original)
        if quarantine.exists() and not obsolete.exists():
            shutil.move(str(quarantine), str(obsolete))
        raise
    return {"status": "REMOVED_FROM_PRODUCTION", "modified": TARGET,
            "quarantined": quarantine.name, "legacy_adapter_import": False,
            "generic_replacement_added": False, "full_pytest_run": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(install(args.root.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
