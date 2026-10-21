"""Install the structured generator converter against the DB-priority selector."""
from pathlib import Path
import ast
import shutil

root = Path.cwd()
bundle = Path(__file__).resolve().parent
source_file = root / "phase165_r55_nk_only_goal.py"
source = source_file.read_text(encoding="utf-8-sig")
new_function = (bundle / "registered_group_goal_candidates.py.txt").read_text(encoding="utf-8")
module = ast.parse(source)
functions = [node for node in module.body if isinstance(node, ast.FunctionDef)
             and node.name == "registered_group_goal_candidates"]
if len(functions) != 2:
    raise RuntimeError("Expected original and override registered_group_goal_candidates; no changes made")
node = functions[-1]
old_function = ast.get_source_segment(source, node)
if "_phase165_r57_r8_previous_registered_group_goal_candidates" not in old_function:
    raise RuntimeError("Unexpected final selector implementation; no changes made")
if "database_group_goal_candidates(n=n, k=k)" not in old_function:
    raise RuntimeError("DB-priority candidate selector missing; no changes made")
lines = source.splitlines(keepends=True)
updated = "".join(lines[:node.lineno-1]) + new_function.rstrip() + "\n" + "".join(lines[node.end_lineno:])
ast.parse(updated)
backup = root / "phase166_r3aj_structured_generator_backup"
backup.mkdir(exist_ok=True)
if source != updated:
    shutil.copy2(source_file, backup / source_file.name)
    source_file.write_text(updated, encoding="utf-8")
    print("PATCHED:", source_file)
else:
    print("ALREADY_APPLIED:", source_file)
target = root / "phase166_r3aj_structured_generator.py"
shutil.copy2(bundle / target.name, target)
print("INSTALLED:", target)
