"""Idempotent R19 installer; modify only existing shared-search function."""
import ast
import shutil
from pathlib import Path

root = Path.cwd()
package = Path(__file__).resolve().parent
source = root / "phase165_r52_r9_shared_math.py"
if not source.exists() or not (root / "phase165_r52_r18_proof_order.py").exists():
    raise SystemExit("Run from repository root after R18 installation")
original = source.read_text(encoding="utf-8")
parsed = ast.parse(original)
functions = [node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "search_shared_group_goal"]
if len(functions) != 1 or not any(arg.arg == "proof_use_order" for arg in functions[0].args.kwonlyargs):
    raise SystemExit("Expected R18 search_shared_group_goal with proof_use_order")
anchor = "    if proof_use_order is not None:\n        from phase165_r52_r18_proof_order import restrict_by_proof_use_order\n"
insertion = (
    "    if proof_use_order == \"registered\":\n"
    "        from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order\n"
    "        proof_use_order = resolve_registered_proof_use_order(proof_context, goal)\n"
)
if insertion not in original:
    if original.count(anchor) != 1:
        raise SystemExit("Unexpected R18 filter block; no changes installed")
    updated = original.replace(anchor, insertion + anchor, 1)
else:
    updated = original
ast.parse(updated)
for name in ("phase165_r52_r19_prop51_binding.py", "test_phase165_r52_r19_prop51_binding.py"):
    shutil.copy2(package / name, root / name)
if updated != original:
    backup = source.with_name("phase165_r52_r9_shared_math.r19_before.py.bak")
    shutil.copy2(source, backup)
    source.write_text(updated, encoding="utf-8")
    print("Updated:", source.name)
else:
    print("Already installed:", source.name)
print("R19 registered proof-use policy available (opt-in: proof_use_order='registered')")
