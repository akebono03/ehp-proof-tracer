from __future__ import annotations
import ast
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
    raise RuntimeError("Expected exactly one renderer function; no patch applied")
node = functions[0]
existing = "".join(original.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])
if "typed_sentence" not in existing or "QuotientIsomorphismStatement" not in existing:
    raise RuntimeError("R3-23 prerequisite missing; no patch applied")
newline = "\r\n" if "\r\n" in original else "\n"
replacement = fragment.replace("\n", newline)
lines = original.splitlines(keepends=True)
backup_dir = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup_dir / target.name)
updated = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
ast.parse(updated)
target.write_bytes(updated.encode("utf-8"))
print("PATCHED:", target)
print("BACKUP:", backup_dir / target.name)
print("FULL_FUNCTION:", package / "render_model_backed_narrative_markdown_FULL.py")
