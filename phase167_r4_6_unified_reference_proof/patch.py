from __future__ import annotations
import ast
from datetime import datetime
from pathlib import Path
import shutil

TARGET = Path('toda_group_proof_narrative_contribution_renderer.py')

INSERT_FUNCTION = '_insert_toda_group_proof_narrative_argument_contributions'
LINK_FUNCTION = 'link_toda_group_proof_narrative_reference_body_consumers'

INSERT_ANCHOR = '  insertions_by_index = {}\n\n  for argument_index, contributions in enumerate('
INSERT_REPLACEMENT = '  # A cited general statement remains a proof premise and belongs to the\n  # Reference section. Its typed specialization is the visible body step.\n  from proof import ProofRule\n  from phase165_r57_r20_general_specialization import (\n    specialize_typed_statement,\n  )\n\n  specialized_source_ids = {\n    id(source_step)\n    for contributions in ordered_contributions\n    for contribution in contributions\n    for source_step in contribution.proof_step.premises\n    if (\n      source_step.rule is ProofRule.GIVEN\n      and contribution.proof_step.rule is ProofRule.INFERENCE\n      and specialize_typed_statement(\n        source_step.conclusion,\n        contribution.proof_step.conclusion,\n      ) is not None\n    )\n  }\n  insertions_by_index = {}\n\n  for argument_index, contributions in enumerate('
SKIP_ANCHOR = '    for contribution_index, contribution in enumerate(\n      contributions\n    ):\n      contribution_line = ('
SKIP_REPLACEMENT = '    for contribution_index, contribution in enumerate(\n      contributions\n    ):\n      if id(contribution.proof_step) in specialized_source_ids:\n        continue\n      contribution_line = ('

CONNECTOR_ANCHOR = '      connector = (\n        connector_by_target_step_id.get(\n          id(\n            contribution.proof_step\n          )\n        )\n      )\n      lines = []'
CONNECTOR_REPLACEMENT = '      connector = (\n        connector_by_target_step_id.get(\n          id(\n            contribution.proof_step\n          )\n        )\n      )\n      if any(\n        id(premise) in specialized_source_ids\n        and specialize_typed_statement(\n          premise.conclusion,\n          contribution.proof_step.conclusion,\n        ) is not None\n        for premise in contribution.proof_step.premises\n      ):\n        connector = None\n      lines = []'

LINK_ANCHOR = '  lines = body_markdown.splitlines()\n\n  for reference_number, source_steps in ('
LINK_REPLACEMENT = '  lines = body_markdown.splitlines()\n\n  # Typed specialization uses the same citation route as any direct\n  # reference application. The general statement stays in Reference.\n  from proof import ProofRule\n  from phase165_r57_r20_general_specialization import (\n    specialize_typed_statement,\n  )\n\n  for reference_number, source_steps in source_steps_by_number.items():\n    marker = "[R" + str(reference_number) + "]"\n    specialized_lines = []\n    for source_step in source_steps:\n      if source_step.rule is not ProofRule.GIVEN:\n        continue\n      for edge in presentation.edges:\n        if edge.premise_step is not source_step:\n          continue\n        derived_step = edge.parent_step\n        if derived_step.rule is not ProofRule.INFERENCE:\n          continue\n        if specialize_typed_statement(\n          source_step.conclusion,\n          derived_step.conclusion,\n        ) is None:\n          continue\n        derived_line = _render_generic_narrative_step(derived_step)\n        if not derived_line:\n          continue\n        indexes = tuple(\n          i for i, line in enumerate(lines)\n          if line.strip().rstrip(".") in (\n            derived_line.strip().rstrip("."),\n            "これより, " + derived_line.strip().rstrip("."),\n          )\n        )\n        if len(indexes) == 1:\n          specialized_lines.append((indexes[0], derived_line.strip()))\n    specialized_lines = list(dict.fromkeys(specialized_lines))\n    if len(specialized_lines) != 1:\n      continue\n    index, derived_line = specialized_lines[0]\n    # The source is not rendered in the proof by the insertion path.\n    # Leave all other, potentially explanatory, paragraphs untouched.\n    source_formulas = {\n      _render_generic_narrative_step(step).strip().rstrip(".")\n      for step in source_steps\n      if _render_generic_narrative_step(step)\n    }\n    for old_index in range(len(lines) - 1, -1, -1):\n      if old_index == index:\n        continue\n      line = lines[old_index].strip().rstrip(".")\n      if any(line == marker + "より, " + formula for formula in source_formulas):\n        del lines[old_index]\n        if old_index < index:\n          index -= 1\n    lines[index] = marker + "より, " + derived_line.rstrip(".") + "."\n\n  for reference_number, source_steps in ('


def get_function(source, name):
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError('target function not unique: ' + name)
    node = nodes[0]
    return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def replace_in_function(source, name, old, new):
    method = get_function(source, name)
    if old not in method:
        if new in method:
            return source
        raise RuntimeError('anchor absent: ' + name)
    if method.count(old) != 1:
        raise RuntimeError('anchor not unique: ' + name)
    modified = method.replace(old, new, 1)
    return source.replace(method, modified, 1)


def main():
    with TARGET.open('r', encoding='utf-8', newline='') as stream:
        original = stream.read()
    patched = replace_in_function(original, INSERT_FUNCTION, INSERT_ANCHOR, INSERT_REPLACEMENT)
    patched = replace_in_function(patched, INSERT_FUNCTION, SKIP_ANCHOR, SKIP_REPLACEMENT)
    patched = replace_in_function(patched, INSERT_FUNCTION, CONNECTOR_ANCHOR, CONNECTOR_REPLACEMENT)
    patched = replace_in_function(patched, LINK_FUNCTION, LINK_ANCHOR, LINK_REPLACEMENT)
    ast.parse(patched)
    if patched != original:
        backup = Path('phase167_r4_6_unified_reference_proof_backup') / datetime.now().strftime('%Y%m%dT%H%M%S') / TARGET.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET, backup)
        with TARGET.open('w', encoding='utf-8', newline='') as out:
            out.write(patched)
        print('PATCHED:', TARGET.resolve())
        print('BACKUP:', backup.resolve())
    else:
        print('ALREADY_PATCHED:', TARGET.resolve())
    for name in (INSERT_FUNCTION, LINK_FUNCTION):
        path = Path('phase167_r4_6_unified_reference_proof') / (name + '_full.py')
        path.write_text(get_function(patched, name), encoding='utf-8')
        print('FULL_FUNCTION:', path.resolve())


if __name__ == '__main__':
    main()
