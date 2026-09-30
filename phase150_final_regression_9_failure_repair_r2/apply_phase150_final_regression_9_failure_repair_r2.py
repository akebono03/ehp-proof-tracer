from pathlib import Path
import ast
import shutil

repo = Path.cwd()
package = Path(__file__).resolve().parent
target = repo / "tests" / "test_phase150_rc4_5_visible_reasons.py"
backup_dir = repo / "phase150_final_regression_9_failure_repair_r2_backup"
backup_dir.mkdir(parents=True, exist_ok=True)
backup = backup_dir / target.name

if not target.exists():
  raise SystemExit(f"Missing target: {target}")

if not backup.exists():
  shutil.copy2(target, backup)

text = target.read_text(encoding="utf-8")
tree = ast.parse(text)
function_name = "test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count"

node = next(
  (
    item
    for item in tree.body
    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    and item.name == function_name
  ),
  None,
)
if node is None:
  raise SystemExit(f"Function not found: {function_name}")

start_node = node.decorator_list[0] if node.decorator_list else node
start = start_node.lineno - 1
end = node.end_lineno

lines = text.splitlines(keepends=True)
replacement = (
  package / "replacement_function.py.txt"
).read_text(encoding="utf-8").rstrip() + "\n"

new_text = "".join(lines[:start]) + replacement + "".join(lines[end:])
ast.parse(new_text)
target.write_text(new_text, encoding="utf-8")

print(f"Replaced whole function: {target}::{function_name}")
print("Production code changes: none")
print("Other test files changed: none")
