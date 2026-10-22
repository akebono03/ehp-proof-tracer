from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent.parent
PACKAGE=Path(__file__).resolve().parent
TARGET=ROOT/'toda_group_proof_narrative_renderer.py'
BACKUP=PACKAGE/'renderer_before.py.bak'
FULL=PACKAGE/'modified_function_full.py.txt'
source=TARGET.read_text(encoding='utf-8-sig')
module=ast.parse(source)
items=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='render_toda_group_proof_narrative_markdown']
if len(items)!=1:
    raise RuntimeError('Renderer must have exactly one existing function')
fn=items[0]
lines=source.splitlines(keepends=True)
last=fn.body[-1]
if not isinstance(last,ast.Return) or not isinstance(last.value,ast.Name) or last.value.id!='rendered' or lines[last.lineno-1].strip()!='return rendered':
    raise RuntimeError('Unexpected renderer return: no patch applied')
body=''.join(lines[fn.lineno-1:fn.end_lineno])
if 'suppressed_inference_labels' not in body:
    raise RuntimeError('R4-1 must be installed first: no patch applied')
if 'typed_display_duplicates' in body:
    raise RuntimeError('R4-2 already present')
fragment='  # R4-2: suppress a duplicate eta-definition display only when\n  # a typed generator-suspension proof step establishes the same identity.\n  # Keep the generator-suspension display and all underlying ProofSteps.\n  if proof_root is not None:\n    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension\n    from toda_rules import TodaEtaFamilyDefinitionStatement\n    from toda_human_readable_renderer import render_toda_expression_latex\n    typed_display_duplicates = set()\n    definitions = [\n      step.conclusion for step in ancestry\n      if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)\n    ]\n    suspensions = [\n      step.conclusion for step in ancestry\n      if isinstance(step.conclusion, GeneratorSuspension)\n    ]\n    for definition in definitions:\n      iterated = definition.iterated_suspension\n      if getattr(iterated, "exponent", None) != 1:\n        continue\n      if any(\n        suspension.source_generator == iterated.expression\n        and suspension.target_generator == definition.element\n        for suspension in suspensions\n      ):\n        lhs = render_toda_expression_latex(definition.element)\n        rhs = "E" + render_toda_expression_latex(iterated.expression)\n        typed_display_duplicates.add((lhs + "=" + rhs).replace(" ", ""))\n    if typed_display_duplicates:\n      retained = []\n      removed = 0\n      for line in rendered.splitlines(keepends=True):\n        normalized = line.strip().strip("$").rstrip(".").replace(" ", "")\n        if normalized in typed_display_duplicates:\n          removed += 1\n          continue\n        retained.append(line)\n      if removed != len(typed_display_duplicates):\n        raise ValueError("R4-2: typed duplicate display does not match the completed narrative")\n      rendered = "".join(retained)\n'
updated=''.join(lines[:last.lineno-1])+fragment+''.join(lines[last.lineno-1:])
ast.parse(updated)
shutil.copy2(TARGET,BACKUP)
TARGET.write_text(updated,encoding='utf-8')
full_lines=updated.splitlines(keepends=True)
FULL.write_text(''.join(full_lines[fn.lineno-1:fn.end_lineno+len(fragment.splitlines())]),encoding='utf-8')
print('PATCHED: existing render_toda_group_proof_narrative_markdown')
print('FULL FUNCTION:',FULL)
