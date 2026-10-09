from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_transport_link.py"
REPLACEMENT = Path(__file__).resolve().parent / "replacement.py"

original = TARGET.read_text(encoding="utf-8")
module = ast.parse(original)
functions = [item for item in module.body if isinstance(item, ast.FunctionDef) and item.name == "render_suspension_transport_link"]
if len(functions) != 1:
    raise RuntimeError("Expected exactly one render_suspension_transport_link function")
fn = functions[0]
current = "".join(original.splitlines(keepends=True)[fn.lineno - 1:fn.end_lineno])
if "destination_matches" in current:
    print("Already applied: R10-R7 Repair 1")
    raise SystemExit(0)
if "_concrete_toda_group_matches_structural_group" not in current:
    raise RuntimeError("Expected R10-R7 base modification; patch was not applied")
if "from proof import ProofStep\n" not in original:
    raise RuntimeError("Expected original ProofStep import")

source = REPLACEMENT.read_text(encoding="utf-8")
next_module = ast.parse(source)
new_fn = next(item for item in next_module.body if isinstance(item, ast.FunctionDef) and item.name == "render_suspension_transport_link")
new_text = "".join(source.splitlines(keepends=True)[new_fn.lineno - 1:new_fn.end_lineno])
updated = original.replace("from proof import ProofStep\n", "from proof import ProofStep\n", 1).replace(current, new_text, 1)
ast.parse(updated)
backup = TARGET.with_suffix(".py.phase162_r10_r7_repair1.bak")
shutil.copy2(TARGET,backup)
TARGET.write_text(updated,encoding="utf-8")
print("Updated:",TARGET)
print("Backup:",backup)
