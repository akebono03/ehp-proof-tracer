from pathlib import Path
import ast
import shutil

repo = Path.cwd()
package = Path(__file__).resolve().parent
backup = repo / "phase150_final_regression_9_failure_repair_backup"
backup.mkdir(parents=True, exist_ok=True)

for filename in (
  "test_phase148_rc2_4_repair_r5.py",
  "test_phase148_rc2_4_repair_r5_r2.py",
):
  target = repo / "tests" / filename
  source = package / "replacement" / filename
  if not target.exists():
    raise SystemExit(f"Missing target: {target}")
  backup_target = backup / filename
  if not backup_target.exists():
    shutil.copy2(target, backup_target)
  shutil.copy2(source, target)
  print(f"Replaced full file: {target}")

rc45 = repo / "tests" / "test_phase150_rc4_5_visible_reasons.py"
if not rc45.exists():
  raise SystemExit(f"Missing target: {rc45}")

backup_rc45 = backup / rc45.name
if not backup_rc45.exists():
  shutil.copy2(rc45, backup_rc45)

text = rc45.read_text(encoding="utf-8")
tree = ast.parse(text)
target_name = "test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count"
node = next(
  (
    item
    for item in tree.body
    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    and item.name == target_name
  ),
  None,
)
if node is None:
  raise SystemExit(f"Function not found: {target_name}")

start_node = node.decorator_list[0] if node.decorator_list else node
start = start_node.lineno - 1
end = node.end_lineno

lines = text.splitlines(keepends=True)
replacement = (
  package
  / "replacement"
  / "rc4_5_replacement_function.py.txt"
).read_text(encoding="utf-8").rstrip() + "\n"

new_text = "".join(lines[:start]) + replacement + "".join(lines[end:])
ast.parse(new_text)
rc45.write_text(new_text, encoding="utf-8")
print(f"Replaced whole function: {rc45}::{target_name}")
print("Production code changes: none")
