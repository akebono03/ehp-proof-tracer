"""R18 minimal, repeatable installation. Requires R17/R16 already installed."""
from __future__ import annotations

import ast
import shutil
from pathlib import Path

root = Path.cwd()
package = Path(__file__).resolve().parent
source = root / "phase165_r52_r9_shared_math.py"
if not source.exists() or not (root / "phase165_r52_r16_web_citation_gate.py").exists():
    raise SystemExit("Run from repository root with R16/R17 installed")
text = source.read_text(encoding="utf-8")
tree = ast.parse(text)
nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "search_shared_group_goal"]
if len(nodes) != 1:
    raise SystemExit("Expected one search_shared_group_goal")
node = nodes[0]
args = node.args.kwonlyargs
if not any(arg.arg == "proof_use_order" for arg in args):
    import re
    lines = text.splitlines(keepends=True)
    header = "".join(lines[node.lineno - 1:node.body[0].lineno - 1])
    match = re.search(r"(def\s+search_shared_group_goal\s*\()(.*?)(\)\s*(?:->\s*[^:]+)?\s*:)", header, re.DOTALL)
    if match is None:
        raise SystemExit("Cannot parse shared search signature")
    arg_text = match.group(2)
    suffix = "proof_use_order=None"
    if arg_text.rstrip().endswith(","):
        arg_text += " " + suffix
    else:
        arg_text += ", " + suffix
    new_header = header[:match.start()] + match.group(1) + arg_text + match.group(3) + header[match.end():]
    text = text.replace(header, new_header, 1)
if "proof_context = restrict_by_proof_use_order(" not in text:
    anchor = "    if expansion_provider is None:\n        expansion_provider = shared_expansion_provider(proof_context)"
    if text.count(anchor) != 1:
        raise SystemExit("Unexpected R16 search context; no changes installed")
    insertion = (
        "    if proof_use_order is not None:\n"
        "        from phase165_r52_r18_proof_order import restrict_by_proof_use_order\n"
        "        proof_context = restrict_by_proof_use_order(\n"
        "            proof_context, goal=goal, policy=proof_use_order,\n"
        "        )\n"
    )
    text = text.replace(anchor, insertion + anchor, 1)
ast.parse(text)
for name in ("phase165_r52_r18_proof_order.py", "test_phase165_r52_r18_proof_order.py"):
    shutil.copy2(package / name, root / name)
if text != source.read_text(encoding="utf-8"):
    shutil.copy2(source, source.with_name("phase165_r52_r9_shared_math.r18_before.py.bak"))
    source.write_text(text, encoding="utf-8")
    print("Updated:", source.name)
else:
    print("Already installed:", source.name)
print("R18 opt-in proof-use order installed")
