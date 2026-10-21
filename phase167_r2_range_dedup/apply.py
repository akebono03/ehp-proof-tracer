from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
folder = Path(__file__).resolve().parent
target = repo / "toda_group_proof_narrative_references.py"
source = target.read_text(encoding="utf-8")
tree = ast.parse(source)
name = "render_toda_group_proof_narrative_reference_entries_markdown"
functions = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == name]
if len(functions) != 1:
    raise RuntimeError("Reference renderer function is not unique")
node = functions[0]
lines = source.splitlines(keepends=True)
start = sum(map(len, lines[:node.lineno - 1]))
end = sum(map(len, lines[:node.end_lineno]))
function = source[start:end]

old = """        if range_suffix not in statement_line:
"""
new = """        # An already embedded condition, e.g. \\\\quad(n \\\\ge 1),
        # must not be appended a second time as separate inline math.
        existing_condition = "(" + applicable_ranges[0].strip() + ")"
        if (
          range_suffix not in statement_line
          and existing_condition not in statement_line
        ):
"""
if function.count(old) != 1:
    raise RuntimeError("Expected unique existing range-append block. No changes made.")
if 'general_formula_by_component' not in function:
    raise RuntimeError("Phase 167 R2 unified renderer is not installed. No changes made.")
changed_function = function.replace(old, new, 1)
updated = source[:start] + changed_function + source[end:]
ast.parse(updated)
backup = folder / "backup" / target.name
backup.parent.mkdir(exist_ok=True, parents=True)
shutil.copy2(target, backup)
target.write_text(updated, encoding="utf-8")
(folder / "modified_function_full.py").write_text(changed_function, encoding="utf-8")
print(json.dumps({
    "status": "PATCHED",
    "file": str(target),
    "function": name,
    "backup": str(backup),
    "full_function": str(folder / "modified_function_full.py"),
}, ensure_ascii=False, indent=2))
