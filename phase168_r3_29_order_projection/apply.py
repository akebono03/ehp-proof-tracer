from __future__ import annotations
import ast
from datetime import datetime
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_5_model_renderer.py"
added = project / "phase168_r3_29_order_projection.py"
original = target.read_text(encoding="utf-8")
nodes = [n for n in ast.parse(original).body if isinstance(n, ast.FunctionDef)
         and n.name == "render_model_backed_narrative_markdown"]
if len(nodes) != 1:
    raise RuntimeError("Expected exactly one model-backed renderer")
node = nodes[0]
lines = original.splitlines(keepends=True)
function = "".join(lines[node.lineno - 1:node.end_lineno])
required = ("project_exactness_chains(model)", "postponed_quotients", "typed_sentence(step.conclusion, step)")
if not all(part in function for part in required):
    raise RuntimeError("R3-28 renderer prerequisite not satisfied: no modifications")
if added.exists():
    raise RuntimeError("Order projection already exists: no modifications")
replacement = (package / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
module = (package / "phase168_r3_29_order_projection.py").read_text(encoding="utf-8")
ast.parse(replacement)
ast.parse(module)
newline = "\r\n" if "\r\n" in original else "\n"
updated = "".join(lines[:node.lineno - 1]) + replacement.replace("\n", newline) + "".join(lines[node.end_lineno:])
ast.parse(updated)
backup = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup / target.name)
added.write_text(module, encoding="utf-8")
target.write_bytes(updated.encode("utf-8"))
print("PATCHED:", target)
print("ADDED:", added)
print("BACKUP:", backup / target.name)
print("FULL FUNCTION:", package / "render_model_backed_narrative_markdown_FULL.py")
