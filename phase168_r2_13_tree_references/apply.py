"""Phase 168 R2-13: minimal proof-tree grounded final references patch."""
from __future__ import annotations
import ast
from dataclasses import replace
from pathlib import Path
import shutil
import sys

TARGET = 'toda_group_proof_narrative_contribution_renderer.py'
FUNCTION = 'render_toda_group_proof_narrative_multi_argument_with_contributions_markdown'
MARKER = '  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n'
INSERT = '''  # Phase 168 R2-13: final citations come from the proven dependency tree,
  # not the already rendered Markdown or visible-step selection.
  tree_reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reachable_step_ids = set()
  pending_steps = [presentation.root_step]
  while pending_steps:
    pending_step = pending_steps.pop()
    if id(pending_step) in reachable_step_ids:
      continue
    reachable_step_ids.add(id(pending_step))
    pending_steps.extend(pending_step.premises)

  tree_reference_entries = tuple(
    replace(
      entry,
      proof_steps=tuple(
        step for step in entry.proof_steps
        if id(step) in reachable_step_ids
      ),
    )
    for entry in tree_reference_entries
    if any(id(step) in reachable_step_ids for step in entry.proof_steps)
  )
  tree_reference_entries = tuple(
    replace(entry, number=number)
    for number, entry in enumerate(tree_reference_entries, start=1)
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = _select_toda_group_proof_narrative_reference_entries_and_statement_lines(
    presentation,
    tree_reference_entries,
  )

'''


def patch_text(text: str) -> tuple[str, str]:
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == FUNCTION]
    if len(functions) != 1:
        raise RuntimeError('expected exactly one target function')
    node = functions[0]
    lines = text.splitlines(keepends=True)
    function_text = ''.join(lines[node.lineno - 1:node.end_lineno])
    if 'Phase 168 R2-13: final citations' in function_text:
        raise RuntimeError('already patched; refusing repeated modification')
    if function_text.count(MARKER) != 1:
        raise RuntimeError('final reference section anchor did not match')
    new_function = function_text.replace(MARKER, INSERT + MARKER, 1)
    new_text = ''.join(lines[:node.lineno - 1]) + new_function + ''.join(lines[node.end_lineno:])
    ast.parse(new_text)
    return new_text, new_function


def main():
    project = Path.cwd()
    script_dir = Path(__file__).resolve().parent
    target = project / TARGET
    if not target.is_file():
        raise SystemExit(f'MISSING: {target}; run from project root')
    source = target.read_text(encoding='utf-8')
    updated, function = patch_text(source)
    output = script_dir / 'output'
    output.mkdir(exist_ok=True)
    backup = output / (TARGET + '.before')
    if backup.exists():
        raise SystemExit('Backup already exists; refusing overwrite')
    shutil.copy2(target, backup)
    (output / 'modified_function_full.py').write_text(function, encoding='utf-8')
    target.write_text(updated, encoding='utf-8')
    print('PATCHED:', target)
    print('BACKUP:', backup)
    print('FULL_FUNCTION:', output / 'modified_function_full.py')


if __name__ == '__main__':
    main()
