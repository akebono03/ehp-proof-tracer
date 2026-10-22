from pathlib import Path
import ast
import shutil
import datetime

ROOT=Path.cwd()
TARGET=ROOT/'toda_group_proof_narrative_argument_body_renderer.py'
assert TARGET.is_file(),TARGET
old=TARGET.read_text(encoding='utf-8')
assert 'def render_toda_group_proof_narrative_argument_body_markdown(' in old
assert 'def _phase167_r4_2_typed_display_equality_key(' not in old
ast.parse(old)
marker='def render_toda_group_proof_narrative_argument_body_markdown('
helper='''def _phase167_r4_2_typed_display_equality_key(statement):
  """A structural equality key for displayed suspension identities.

  Compare typed generators, not generator names or rendered TeX.  Return
  None for claims whose equality cannot be established structurally.
  """
  from expression import HomotopyElement, IteratedSuspension
  from homotopy_groups import TodaSuspensionMap

  def element_key(element):
    if not isinstance(element, HomotopyElement):
      return None
    symbol = element.generator
    if symbol is None:
      return None
    return (
      type(element), type(symbol), symbol.family, symbol.index,
      symbol.decoration, element.dimension, element.source, element.target,
    )

  if isinstance(getattr(statement, "map", None), TodaSuspensionMap):
    source = getattr(statement, "source_generator", None)
    target = getattr(statement, "target_generator", None)
    source_key = element_key(source)
    target_key = element_key(target)
    if source_key is not None and target_key is not None:
      group_map = statement.map
      if (
        (source.source, source.target)
        == (group_map.source_group.group_dimension,
            group_map.source_group.sphere_dimension)
        and (target.source, target.target)
        == (group_map.target_group.group_dimension,
            group_map.target_group.sphere_dimension)
      ):
        return ("one_suspension", frozenset((
          ("source", source_key), ("target", target_key),
        )))

  suspension = getattr(statement, "iterated_suspension", None)
  target = getattr(statement, "element", None)
  if isinstance(suspension, IteratedSuspension) and suspension.exponent == 1:
    source = suspension.expression
    source_key = element_key(source)
    target_key = element_key(target)
    if source_key is not None and target_key is not None:
      if (
        isinstance(source.source, int)
        and isinstance(source.target, int)
        and isinstance(target.source, int)
        and isinstance(target.target, int)
        and target.source == source.source + 1
        and target.target == source.target + 1
      ):
        return ("one_suspension", frozenset((
          ("source", source_key), ("target", target_key),
        )))
  return None


'''
assert old.count(marker)==1
new=old.replace(marker,helper+marker,1)
head='  lines = []\n  connector_inserted = False\n  owned_primary_exactness_inserted = False\n'
assert new.count(head)==1
new=new.replace(head,'  displayed_equality_keys = set()\n'+head,1)
needle='''      if not display_steps:
        continue
'''
assert new.count(needle)==1
insertion='''      unique_steps = []
      for proof_step in display_steps:
        equality_key = _phase167_r4_2_typed_display_equality_key(
          proof_step.conclusion
        )
        if (
          equality_key is not None
          and equality_key in displayed_equality_keys
        ):
          continue
        unique_steps.append(proof_step)
        if equality_key is not None:
          displayed_equality_keys.add(equality_key)
      display_steps = tuple(unique_steps)

'''
new=new.replace(needle,insertion+needle,1)
ast.parse(new)
backup=ROOT/'phase167_r4_2_general_typed_dedup_backup'
backup.mkdir(exist_ok=True)
backup_file=backup/'original_argument_body_renderer.py'
if not backup_file.exists():
    shutil.copy2(TARGET,backup_file)
TARGET.write_text(new,encoding='utf-8')
module=ast.parse(new)
output=ROOT/'phase167_r4_2_general_typed_dedup'/'modified_functions_full.py.txt'
parts=[]
for node in module.body:
    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name in ('_phase167_r4_2_typed_display_equality_key','render_toda_group_proof_narrative_argument_body_markdown'):
        parts.append(''.join(new.splitlines(keepends=True)[node.lineno-1:node.end_lineno]))
output.write_text('\n\n'.join(parts),encoding='utf-8')
print('PATCHED:',TARGET)
print('FULL FUNCTIONS:',output)
