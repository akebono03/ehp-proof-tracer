from __future__ import annotations
import ast
from datetime import datetime
from pathlib import Path
import shutil

ROOT = Path.cwd()
TARGET = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
PACKAGE = Path(__file__).resolve().parent
OLD_START = '  # Typed specialization uses the same citation route as any direct\n'
OLD_END = '  for reference_number, source_steps in (\n    source_steps_by_number.items()\n  ):\n'
NEW_BLOCK = '''  # Connect already-derived, single-premise proof steps to their cited
  # literature premises. Do not repeat specialization or inspect rule names.
  from proof import ProofRule

  for reference_number, source_steps in source_steps_by_number.items():
    marker = "[R" + str(reference_number) + "]"
    source_ids = {
      id(step)
      for step in source_steps
      if step.rule is ProofRule.GIVEN
    }
    consumers = []
    for edge in presentation.edges:
      if id(edge.premise_step) not in source_ids:
        continue
      derived_step = edge.parent_step
      if derived_step.rule is not ProofRule.INFERENCE:
        continue
      if (
        len(derived_step.premises) != 1
        or derived_step.premises[0] is not edge.premise_step
      ):
        continue
      derived_line = _render_generic_narrative_step(derived_step)
      if not derived_line:
        continue
      candidates = tuple(
        i for i, line in enumerate(lines)
        if line.strip().rstrip(".。") in (
          derived_line.strip().rstrip(".。"),
          "これより, " + derived_line.strip().rstrip(".。"),
          "これより、" + derived_line.strip().rstrip(".。"),
        )
      )
      if len(candidates) == 1:
        consumers.append((candidates[0], derived_line.strip()))
    consumers = list(dict.fromkeys(consumers))
    if len(consumers) != 1:
      continue
    index, derived_line = consumers[0]
    source_formulas = {
      _render_generic_narrative_step(step).strip().rstrip(".。")
      for step in source_steps
      if _render_generic_narrative_step(step)
    }
    for old_index in range(len(lines) - 1, -1, -1):
      if old_index == index:
        continue
      stripped = lines[old_index].strip().rstrip(".。")
      if any(
        stripped == marker + "より, " + formula
        or stripped == marker + "より、" + formula
        for formula in source_formulas
      ):
        del lines[old_index]
        if old_index < index:
          index -= 1
    lines[index] = marker + "より, " + derived_line.rstrip(".。") + "."

'''

def function_bounds(source: str, name: str) -> tuple[int, int]:
    tree = ast.parse(source)
    matching = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(matching) != 1:
        raise RuntimeError(f'expected exactly one {name}, found {len(matching)}')
    node = matching[0]
    lines = source.splitlines(keepends=True)
    return sum(len(x) for x in lines[:node.lineno - 1]), sum(len(x) for x in lines[:node.end_lineno])

def transform(source: str) -> tuple[str, str]:
    a, b = function_bounds(source, 'link_toda_group_proof_narrative_reference_body_consumers')
    old = source[a:b]
    if old.count(OLD_START) != 1 or old.count(OLD_END) != 1:
        raise RuntimeError('R4-6 function anchors not found uniquely; no modification')
    p = old.index(OLD_START)
    q = old.index(OLD_END, p)
    rewritten = old[:p] + NEW_BLOCK + old[q:]
    if rewritten == old:
        raise RuntimeError('no code change')
    updated = source[:a] + rewritten + source[b:]
    ast.parse(updated)
    return updated, rewritten

def main() -> None:
    if not TARGET.is_file():
        raise SystemExit('ERROR: repository root not found: ' + str(TARGET))
    original = TARGET.read_bytes()
    newline = '\r\n' if b'\r\n' in original else '\n'
    text = original.decode('utf-8-sig').replace('\r\n', '\n')
    updated, function = transform(text)
    backup_dir = ROOT / 'phase167_r4_9_reference_backup' / datetime.now().strftime('%Y%m%dT%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup = backup_dir / TARGET.name
    shutil.copy2(TARGET, backup)
    bom = b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b''
    TARGET.write_bytes(bom + updated.replace('\n', newline).encode('utf-8'))
    (PACKAGE / 'modified_function_full.py').write_text(function, encoding='utf-8')
    print('PATCHED:', TARGET)
    print('BACKUP:', backup)
    print('FULL_FUNCTION:', PACKAGE / 'modified_function_full.py')

if __name__ == '__main__':
    main()
