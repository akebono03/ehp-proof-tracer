from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP = PACKAGE / "renderer_before.py.bak"
FULL = PACKAGE / "modified_function_full.py.txt"

source = TARGET.read_text(encoding="utf-8-sig")
tree = ast.parse(source)
matches = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "render_toda_group_proof_narrative_markdown"
]
if len(matches) != 1:
    raise RuntimeError("The existing renderer function was not found uniquely")
fn = matches[0]
if not isinstance(fn.body[-1], ast.Return) or not isinstance(fn.body[-1].value, ast.Name) or fn.body[-1].value.id != "rendered":
    raise RuntimeError("Unexpected renderer tail; no changes applied")
lines = source.splitlines(keepends=True)
body = "".join(lines[fn.lineno - 1:fn.end_lineno])
if "phase165_r12_r2_quotient_rules" not in body:
    raise RuntimeError("Unexpected existing renderer body; no changes applied")
if "suppressed_inference_labels" in body:
    raise RuntimeError("Typed suppression appears already installed")
if "line.strip() != \"infinite cyclic quotient structure\"" in body:
    raise RuntimeError("Older text-only patch detected; restore it first")

# The decision is made using the conclusion and premise types,
# not by matching a hard-coded English inference-rule name.
insert = (
    "  # Hide only labels of typed finite-cyclic quotient deductions.\n"
    "  # This occurs after the existing mathematical narrative is assembled,\n"
    "  # so existing quotient paragraph/anchor calculations remain unchanged.\n"
    "  if proof_root is not None:\n"
    "    from phase165_r12_r2_quotient_rules import (\n"
    "      CyclicStructureStatement,\n"
    "      QuotientIsomorphismStatement,\n"
    "    )\n"
    "    from proof import ProofRule\n"
    "    suppressed_inference_labels = {\n"
    "      step.inference_rule.name\n"
    "      for step in ancestry\n"
    "      if step.rule is ProofRule.INFERENCE\n"
    "      and step.inference_rule is not None\n"
    "      and isinstance(step.conclusion, CyclicStructureStatement)\n"
    "      and step.conclusion.order is not None\n"
    "      and any(\n"
    "        isinstance(premise.conclusion, QuotientIsomorphismStatement)\n"
    "        for premise in step.premises\n"
    "      )\n"
    "    }\n"
    "    if suppressed_inference_labels:\n"
    "      rendered = \"\".join(\n"
    "        line for line in rendered.splitlines(keepends=True)\n"
    "        if line.strip() not in suppressed_inference_labels\n"
    "      )\n"
)
index = fn.body[-1].lineno-1
if lines[index].strip() != "return rendered":
    raise RuntimeError("Unexpected return position")
new_source = "".join(lines[:index]) + insert + "".join(lines[index:])
ast.parse(new_source)
shutil.copy2(TARGET, BACKUP)
TARGET.write_text(new_source, encoding="utf-8")
new_lines = new_source.splitlines(keepends=True)
FULL.write_text("".join(new_lines[fn.lineno - 1:fn.end_lineno + len(insert.splitlines())]), encoding="utf-8")
print("PATCHED: existing render_toda_group_proof_narrative_markdown")
print("FULL FUNCTION:", FULL)
