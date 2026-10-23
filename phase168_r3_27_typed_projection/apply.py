from __future__ import annotations
import ast
from datetime import datetime
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_5_model_renderer.py"
module_target = project / "phase168_r3_27_typed_statement_projection.py"
current = target.read_text(encoding="utf-8")
nodes = [n for n in ast.parse(current).body if isinstance(n, ast.FunctionDef)
         and n.name == "render_model_backed_narrative_markdown"]
if len(nodes) != 1:
    raise RuntimeError("Expected one renderer; nothing modified")
node = nodes[0]
parts = current.splitlines(keepends=True)
old_function = "".join(parts[node.lineno - 1:node.end_lineno])
required = ("project_exactness_chains(model)", "def typed_sentence(", "postponed_quotients")
if not all(item in old_function for item in required):
    raise RuntimeError("Requires R3-26a renderer; nothing modified")
if module_target.exists():
    raise RuntimeError("Projection module already exists; nothing modified")
module = (package / "phase168_r3_27_typed_statement_projection.py").read_text(encoding="utf-8")
replacement = (package / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
ast.parse(module)
newline = "\r\n" if "\r\n" in current else "\n"
updated = "".join(parts[:node.lineno - 1]) + replacement.replace("\n", newline) + "".join(parts[node.end_lineno:])
ast.parse(updated)
backup = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup / target.name)
module_target.write_text(module, encoding="utf-8")
target.write_bytes(updated.encode("utf-8"))
print("PATCHED", target)
print("ADDED", module_target)
print("BACKUP", backup / target.name)
