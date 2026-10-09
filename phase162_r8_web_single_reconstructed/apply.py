"""Apply only the Web route change, preserving the current local code."""
import ast
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
path = root / 'web_group_proof.py'
source = path.read_text(encoding='utf-8-sig')
module = ast.parse(source)
func = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'build_standard_web_group_proof_view')
lines = source.splitlines(keepends=True)
original = ''.join(lines[func.lineno - 1:func.end_lineno])
anchor = '''  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )'''
replacement = '''  if n == 3 and k == 2 and mode == "narrative":
    from phase162_pi5_3_web_replay import (
      build_phase162_pi5_3_web_replay,
    )
    replay = build_phase162_pi5_3_web_replay(
      max_depth=max(max_depth, 40),
    )
  else:
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=max_depth,
      )
    )'''
if original.count(anchor) != 1:
    raise RuntimeError('Expected original replay selection exactly once')
modified = original.replace(anchor, replacement)
start = '''      if n == 3 and k == 2:
        from phase162_web_narrative_integration import (
          build_phase162_web_validated_isomorphism_markdown,
        )'''
if original.count(start) != 1:
    raise RuntimeError('Expected old second-panel insertion exactly once')
prefix, rest = modified.split(start, 1)
ending = '''
    rendered_lines = (
      _build_group_proof_rendered_lines('''
if ending not in rest:
    raise RuntimeError('Could not find end of second panel block')
_, suffix = rest.split(ending, 1)
modified = prefix + ending + suffix
combined = ''.join(lines[:func.lineno - 1]) + modified + ''.join(lines[func.end_lineno:])
ast.parse(combined)
backup = root / 'web_group_proof.py.phase162_r8_before.bak'
if not backup.exists():
    shutil.copy2(path, backup)
path.write_text(combined, encoding='utf-8')
(Path(__file__).parent / 'modified_function.py').write_text(modified, encoding='utf-8')
print('Updated:', path)
print('Backup:', backup)
print('Full replacement function:', Path(__file__).parent / 'modified_function.py')
