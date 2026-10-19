from __future__ import annotations
import ast
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root / "phase165_r57_r1_single_entry" / "test_phase165_r57_r1_single_entry.py"
source = target.read_text(encoding="utf-8")
tree = ast.parse(source)
name = "test_standard_route_uses_r55_for_arbitrary_nk"
matches = [x for x in tree.body if isinstance(x, (ast.FunctionDef,ast.AsyncFunctionDef)) and x.name == name]
if len(matches) != 1:
    raise SystemExit("FAIL: expected exactly one test function; no edits made")
node = matches[0]
old = "\n".join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
if "def search(*, n, k, goal=None):" in old and "calls.append((n, k, goal))" in old:
    print("ALREADY_APPLIED")
    raise SystemExit(0)
if "def search(*, n, k):" not in old or "calls.append((n, k))" not in old or "assert calls == [(3, 2)]" not in old:
    raise SystemExit("FAIL: unknown local version; no edits made")
new = old.replace("def search(*, n, k):", "def search(*, n, k, goal=None):")
new = new.replace("calls.append((n, k))", "calls.append((n, k, goal))")
new = new.replace("assert calls == [(3, 2)]", "assert calls == [(3, 2, None)]")
if new == old:
    raise SystemExit("FAIL: no change made")
lines = source.splitlines(keepends=True)
original = "".join(lines)
lines[node.lineno-1:node.end_lineno] = [new]
updated = "".join(lines)
ast.parse(updated)
target.write_text(updated,encoding="utf-8",newline="")
print("APPLIED:", target.relative_to(root))
