"""Synchronize the retired provider implementation with its shadowing package module.

No broad refactor, no mathematics or source registry changes.
"""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
ROOT_MODULE = ROOT / "phase165_r52_r7_registered_common_proof.py"
PACKAGE_MODULE = ROOT / "phase165_r52_r7_registered_common_proof" / "phase165_r52_r7_registered_common_proof.py"
REMOVED = ("RegisteredProofProvider", "registered_proof_providers")

def inspect_module(path: Path) -> dict:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    names = {item.name for item in tree.body if isinstance(item, (ast.FunctionDef, ast.ClassDef))}
    funcs = [item for item in tree.body if isinstance(item, ast.FunctionDef)
             and item.name == "build_registered_common_replay"]
    if len(funcs) != 1:
        raise RuntimeError(f"unexpected common replay entry in {path}")
    kw = [arg.arg for arg in funcs[0].args.kwonlyargs]
    return {"source": source, "names": names, "kwonlyargs": kw}

def main() -> None:
    if not ROOT_MODULE.is_file() or not PACKAGE_MODULE.is_file():
        raise FileNotFoundError("expected both root and package production modules")
    root = inspect_module(ROOT_MODULE)
    package = inspect_module(PACKAGE_MODULE)
    if any(name in root["names"] for name in REMOVED) or "providers" in root["kwonlyargs"]:
        raise RuntimeError("root retirement not installed: refusing to synchronize")
    if not {"group_result", "max_depth", "mode"}.issubset(root["kwonlyargs"]):
        raise RuntimeError("unexpected common replay signature")
    if "search_shared_group_goal" not in root["source"]:
        raise RuntimeError("common goal search is missing")
    if any(name in package["names"] for name in REMOVED) or "providers" in package["kwonlyargs"]:
        if "search_shared_group_goal" not in package["source"]:
            raise RuntimeError("package module is not the known old common-replay implementation")
    changed = root["source"] != package["source"]
    if changed:
        backup = PACKAGE_MODULE.with_name(PACKAGE_MODULE.name + ".phase165_r6_1_shadow_before.bak")
        if not backup.exists():
            shutil.copy2(PACKAGE_MODULE, backup)
        PACKAGE_MODULE.write_text(root["source"], encoding="utf-8")
    print(json.dumps({
        "phase": "165 R6-1 package shadow repair",
        "package_module_updated": changed,
        "root_module_unchanged": True,
        "removed_symbols": list(REMOVED),
        "reference_registry_unchanged": True,
        "full_pytest_run": False
    }, indent=2))

if __name__ == "__main__":
    main()
