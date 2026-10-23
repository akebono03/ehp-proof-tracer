from __future__ import annotations
import ast
import hashlib
from datetime import datetime
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_5_model_renderer.py"
fragment = (package / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
original = target.read_text(encoding="utf-8")
tree = ast.parse(original)
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "render_model_backed_narrative_markdown"]
if len(functions) != 1:
    raise RuntimeError("Exactly one renderer function required")
node = functions[0]
lines = original.splitlines(keepends=True)
existing = "".join(lines[node.lineno - 1:node.end_lineno])
if "combined_sequence = None" not in existing or "postponed_quotients" not in existing:
    raise RuntimeError("Expected R3-24 code not found: aborting without changes")
replacement = fragment.replace("\n", "\r\n" if "\r\n" in original else "\n")
updated = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
ast.parse(updated)
backup = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup / target.name)
target.write_bytes(updated.encode("utf-8"))
print("PATCHED:", target)
print("BACKUP:", backup / target.name)
print("NEW SHA256:", hashlib.sha256(target.read_bytes()).hexdigest())
