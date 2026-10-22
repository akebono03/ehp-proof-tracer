from pathlib import Path
import ast
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r4_flask_bridge.py"
PACKAGE = Path(__file__).resolve().parent
NEW_FUNCTION = (PACKAGE / "build_group_proof_progress_view_FULL.py").read_text(encoding="utf-8")

def main():
    if not TARGET.is_file():
        raise SystemExit("ERROR: expected production Flask bridge is absent")
    source = TARGET.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build_group_proof_progress_view"]
    if len(functions) != 1:
        raise SystemExit("ERROR: expected exactly one bridge function")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    old = "".join(lines[node.lineno - 1:node.end_lineno])
    if old.strip() == NEW_FUNCTION.strip():
        print("ALREADY_PATCHED:", TARGET)
        return
    if 'from phase165_r55_nk_only_goal import search_group_from_registered_goal' not in old:
        raise SystemExit("ERROR: function does not match inspected legacy Web route; no change made")
    if 'build_partial_web_group_proof_view(' not in old:
        raise SystemExit("ERROR: unexpected bridge implementation; no change made")
    backup = PACKAGE / "backup" / TARGET.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, backup)
    replacement = NEW_FUNCTION.rstrip() + "\n"
    new_source = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
    ast.parse(new_source)
    TARGET.write_text(new_source, encoding="utf-8")
    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("FULL_FUNCTION:", PACKAGE / "build_group_proof_progress_view_FULL.py")

if __name__ == "__main__":
    main()
