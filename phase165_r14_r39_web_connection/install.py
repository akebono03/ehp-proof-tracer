"""Insert one narrow routing branch, preserving the rest of the existing Web function."""
from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
path = root / "web_group_proof.py"
src = path.read_text(encoding="utf-8")
module = ast.parse(src)
functions = [x for x in module.body if isinstance(x, (ast.FunctionDef,ast.AsyncFunctionDef)) and x.name == "build_standard_web_group_proof_view"]
if len(functions) != 1:
    raise RuntimeError("expected one Web group-proof builder")
f = functions[0]
lines = src.splitlines(keepends=True)
marker = "  if n == 2 and k == 1:\n    from phase165_r14_r39_web_connection import build_phase165_pi32_web_view\n    return build_phase165_pi32_web_view(max_depth=max_depth, mode=mode)\n"
if "build_phase165_pi32_web_view" in src:
    print("R39 route already installed")
else:
    # Insert immediately after the function docstring: all non-pi32 paths untouched.
    doc = f.body[0]
    if not isinstance(doc, ast.Expr) or not isinstance(doc.value, (ast.Constant, ast.Str)):
        raise RuntimeError("expected group view builder docstring")
    pos = doc.end_lineno
    lines.insert(pos, marker)
    updated = "".join(lines)
    compile(updated, str(path), "exec")
    backup = path.with_suffix(".phase165_r39_backup.py")
    backup.write_text(src, encoding="utf-8")
    path.write_text(updated, encoding="utf-8")
    print("R39 Web group-proof route installed; backup:", backup)
