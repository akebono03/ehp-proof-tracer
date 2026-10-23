from __future__ import annotations
import ast
from datetime import datetime
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_5_model_renderer.py"
original = target.read_text(encoding="utf-8")
functions = [node for node in ast.parse(original).body
             if isinstance(node, ast.FunctionDef)
             and node.name == "render_model_backed_narrative_markdown"]
if len(functions) != 1:
    raise RuntimeError("Expected exactly one renderer function; not modifying")
node = functions[0]
lines = original.splitlines(keepends=True)
existing = "".join(lines[node.lineno - 1:node.end_lineno])
if (r'EHP_DELTA_MAP: r"\\Delta"' not in existing
        or r'rf" \\xrightarrow' not in existing
        or "merged_sequences" not in existing):
    raise RuntimeError("Expected R3-25 buggy version not found; not modifying")
replacement = (package / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
newline = "\r\n" if "\r\n" in original else "\n"
updated = "".join(lines[:node.lineno - 1]) + replacement.replace("\n", newline) + "".join(lines[node.end_lineno:])
ast.parse(updated)
backup = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup / target.name)
target.write_bytes(updated.encode("utf-8"))
print("PATCHED", target)
print("BACKUP", backup / target.name)
print("FULL_FUNCTION", package / "render_model_backed_narrative_markdown_FULL.py")
