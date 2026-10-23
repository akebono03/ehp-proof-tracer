from __future__ import annotations
import ast
import hashlib
from datetime import datetime
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_5_model_renderer.py"
new_module = project / "phase168_r3_26_exactness_projection.py"
current = target.read_text(encoding="utf-8")
nodes = [node for node in ast.parse(current).body if isinstance(node, ast.FunctionDef)
         and node.name == "render_model_backed_narrative_markdown"]
if len(nodes) != 1:
    raise RuntimeError("Expected one renderer function; no changes made")
node = nodes[0]
lines = current.splitlines(keepends=True)
old_function = "".join(lines[node.lineno - 1:node.end_lineno]).replace("\r\n", "\n")
expected_digest = "4aafcc0892dcaf7e2cab8a4a7727e00cef944f3d5c6497647a8ea08ac140b5bb"
actual_digest = hashlib.sha256(old_function.encode("utf-8")).hexdigest()
if actual_digest != expected_digest:
    raise RuntimeError("Expected exact R3-25a function; no changes made. "
                       + "Current digest: " + actual_digest)
if new_module.exists():
    raise RuntimeError("Projection module already exists; no changes made")
fragment = (package / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
module_content = (package / "phase168_r3_26_exactness_projection.py").read_text(encoding="utf-8")
ast.parse(fragment)
ast.parse(module_content)
newline = "\r\n" if "\r\n" in current else "\n"
updated = "".join(lines[:node.lineno - 1]) + fragment.replace("\n", newline) + "".join(lines[node.end_lineno:])
ast.parse(updated)
backup = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup / target.name)
new_module.write_text(module_content, encoding="utf-8")
target.write_bytes(updated.encode("utf-8"))
print("PATCHED:", target)
print("ADDED:", new_module)
print("BACKUP:", backup / target.name)
print("FULL_FUNCTION:", package / "render_model_backed_narrative_markdown_FULL.py")
