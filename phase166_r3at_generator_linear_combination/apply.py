from pathlib import Path
import ast
import shutil
import sys

root = Path(__file__).resolve().parent.parent
source = root / "phase166_r3aj_structured_generator.py"
replacement = (Path(__file__).resolve().parent / "replacement_function.py.txt").read_text(encoding="utf-8")
if not source.is_file():
    raise SystemExit("Missing phase166_r3aj_structured_generator.py")
original = source.read_text(encoding="utf-8")
module = ast.parse(original)
matches = [node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "database_structured_group_goal_candidates"]
if len(matches) != 1:
    raise SystemExit("Expected one database_structured_group_goal_candidates function; no changes made")
node = matches[0]
lines = original.splitlines(keepends=True)
updated = "".join(lines[:node.lineno - 1]) + replacement.rstrip() + "\n" + "".join(lines[node.end_lineno:])
ast.parse(updated)
backup_dir = root / "phase166_r3at_generator_linear_combination_backup"
backup_dir.mkdir(exist_ok=True)
shutil.copy2(source, backup_dir / source.name)
source.write_text(updated, encoding="utf-8")
print("PATCHED:", source)
print("BACKUP:", backup_dir / source.name)
print("FULL FUNCTION:", Path(__file__).resolve().parent / "replacement_function.py.txt")
