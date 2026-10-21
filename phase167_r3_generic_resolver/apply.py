from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

folder = Path(__file__).resolve().parent
root = folder.parent
target = root / "phase166_r3t_goal_source_binding" / "goal_source.py"
source = target.read_text(encoding="utf-8")
tree = ast.parse(source)
functions = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "resolve_specialized_goal_citing_id"
]
if len(functions) != 1:
    raise RuntimeError("Expected one resolver function")
node = functions[0]
lines = source.splitlines(keepends=True)
start = sum(map(len, lines[:node.lineno - 1]))
end = sum(map(len, lines[:node.end_lineno]))
old = source[start:end]
if "specialize_eta_group_relation" not in old:
    raise RuntimeError("Unexpected resolver code; refusing patch")
replacement = (folder / "replacement_function.py").read_text(encoding="utf-8").rstrip() + "\n"
updated = source[:start] + replacement + source[end:]
ast.parse(updated)
backup = folder / "backup" / "goal_source.py"
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup)
target.write_text(updated, encoding="utf-8")
print(json.dumps({
    "status": "PATCHED", "target": str(target), "backup": str(backup),
    "replacement_function": str(folder / "replacement_function.py")
}, ensure_ascii=False, indent=2))
