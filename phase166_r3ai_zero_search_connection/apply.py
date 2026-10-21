from pathlib import Path
import ast
import shutil

root = Path.cwd()
bundle = Path(__file__).resolve().parent
backup = root / "phase166_r3ai_zero_search_connection_backup"
changes = (
    ("phase165_r55_nk_only_goal.py", "search_group_from_registered_goal"),
    ("phase165_r52_r2_search_adapter.py", "search_registered_partial_proof"),
)
for file_name, function in changes:
    path = root / file_name
    original = path.read_text(encoding="utf-8-sig")
    replacement = (bundle / (function + ".py.txt")).read_text(encoding="utf-8")
    tree = ast.parse(original)
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == function]
    if len(nodes) != 1:
        raise RuntimeError("Unexpected function count: " + file_name)
    node = nodes[0]
    lines = original.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno-1]) + replacement + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    if updated == original:
        print("ALREADY_APPLIED:", file_name)
        continue
    backup.mkdir(exist_ok=True)
    shutil.copy2(path, backup / file_name)
    path.write_text(updated, encoding="utf-8")
    print("PATCHED:", file_name)
print("BACKUP:", backup)
