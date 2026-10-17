"""Guarded, idempotent Phase 165 R6-2 R4-R8 installation."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r3_recursive_search.py"
HELPER = ROOT / "phase165_r6_2_r4_r8_dedup.py"
MARKER = "append_unique_verified_derivation(options, step)"
OLD = "                        options.append(step)"
NEW = "                        append_unique_verified_derivation(options, step)"
IMPORT = "from phase165_r6_2_r4_r8_dedup import append_unique_verified_derivation\n"


def install():
    if not TARGET.exists():
        raise FileNotFoundError(TARGET)
    data = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in data else "\n"
    source = data.decode("utf-8")
    if MARKER in source:
        if not HELPER.exists():
            shutil.copyfile(Path(__file__).with_name(HELPER.name), HELPER)
        print("ALREADY_INSTALLED")
        return
    tree = ast.parse(source)
    matches = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "reconstruct_registered_goal"]
    if len(matches) != 1:
        raise RuntimeError("canonical function shape changed")
    if source.count(OLD) != 1:
        raise RuntimeError("inference append anchor changed; no files modified")
    if "from phase165_r6_2_r4_r8_dedup import" in source:
        raise RuntimeError("partial prior patch detected")
    import_anchor = "from proof import ProofStep, ProofRule, find_inference_matches_for_rule"
    if source.count(import_anchor) != 1:
        raise RuntimeError("canonical import anchor changed")
    updated = source.replace(import_anchor, import_anchor + newline + IMPORT.strip(), 1).replace(OLD, NEW, 1)
    ast.parse(updated)
    backup = TARGET.with_suffix(".py.r4_r8_before.bak")
    if backup.exists():
        raise RuntimeError("backup already exists but patch marker missing; inspect manually")
    backup.write_bytes(data)
    shutil.copyfile(Path(__file__).with_name(HELPER.name), HELPER)
    TARGET.write_bytes(updated.encode("utf-8"))
    print("INSTALLED")
    print("backup:", backup)
    # Deliver the COMPLETE changed function for audit, not a fragment.
    parsed = ast.parse(updated)
    fn = next(n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == "reconstruct_registered_goal")
    lines = updated.splitlines(keepends=True)
    (Path(__file__).parent / "installed_function_full.py.txt").write_text("".join(lines[fn.lineno - 1:fn.end_lineno]), encoding="utf-8")


if __name__ == "__main__":
    install()
