from __future__ import annotations

import ast
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root / "phase165_r57_r1_single_entry" / "test_phase165_r57_r1_single_entry.py"
source = target.read_text(encoding="utf-8")
tree = ast.parse(source)
matches = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "test_standard_route_real_pi32_public_renderer"
]
if len(matches) != 1:
    raise SystemExit("ERROR: expected one named test; no changes made")
node = matches[0]
parts = source.splitlines(keepends=True)
old = "".join(parts[node.lineno - 1:node.end_lineno])
needle = 'assert "generic-partial-proof" == view.key'
replacement = 'assert view.key == "generic-complete-proof"\n    assert view.partial_result is False'
if replacement in old:
    print("ALREADY_APPLIED")
    raise SystemExit(0)
if old.count(needle) != 1:
    raise SystemExit("ERROR: unexpected test content; no changes made")
new = old.replace(needle, replacement)
parts[node.lineno - 1:node.end_lineno] = [new]
updated = "".join(parts)
ast.parse(updated)
target.write_text(updated, encoding="utf-8", newline="")
print("APPLIED:", target.relative_to(root))
