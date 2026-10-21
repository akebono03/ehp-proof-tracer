from pathlib import Path
import ast
import shutil

repo = Path.cwd()
target = repo / "phase165_r52_r3_web_adapter.py"
function_name = "build_partial_web_group_proof_view"
replacement = (Path(__file__).resolve().parent / (function_name + ".py.txt")).read_text(encoding="utf-8")
source = target.read_text(encoding="utf-8-sig")
tree = ast.parse(source)
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == function_name]
if len(functions) != 1:
    raise RuntimeError("Expected one existing Web adapter function; no modifications made")
node = functions[0]
lines = source.splitlines(keepends=True)
updated = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
ast.parse(updated)
if updated != source:
    backup = repo / "phase166_r3ak_public_target_backup"
    backup.mkdir(exist_ok=True)
    shutil.copy2(target, backup / target.name)
    target.write_text(updated, encoding="utf-8")
    print("PATCHED:", target)
    print("BACKUP:", backup / target.name)
else:
    print("ALREADY_APPLIED:", target)
