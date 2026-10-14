"""Apply only the R52-R14 group-proof root citation guard."""
from pathlib import Path
import shutil
import ast

root = Path.cwd()
source = root / "phase165_r52_r9_shared_math.py"
if not source.is_file():
    raise SystemExit("Missing shared math source; no files modified")
original = source.read_text(encoding="utf-8")
tree = ast.parse(original)
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "search_shared_group_goal"]
if len(functions) != 1:
    raise SystemExit("Expected exactly one search_shared_group_goal; no changes made")
node = functions[0]
lines = original.splitlines(keepends=True)
old = "".join(lines[node.lineno - 1: node.end_lineno])
new = (Path(__file__).resolve().parent / "search_shared_group_goal.txt").read_text(encoding="utf-8")
if "excluded_ids = {" in old:
    print("R52-R14 already installed")
else:
    if "return search_registered_partial_proof(" not in old or "goal = Relation(" not in old:
        raise SystemExit("Unexpected function shape; no changes made")
    if original.count(old) != 1:
        raise SystemExit("Unexpected duplicate body; no changes made")
    patched = original.replace(old, new.rstrip("\n"), 1)
    ast.parse(patched)
    backup = root / "phase165_r52_r9_shared_math.py.r52_r14_backup"
    if not backup.exists():
        shutil.copy2(source, backup)
    source.write_text(patched, encoding="utf-8")
    print("Updated: phase165_r52_r9_shared_math.py")
package = Path(__file__).resolve().parent
shutil.copy2(package / "test_phase165_r52_r14_root_dependency_guard.py", root / "test_phase165_r52_r14_root_dependency_guard.py")
print("R52-R14 root self-citation guard installed")
