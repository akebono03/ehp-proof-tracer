"""R27-R33: replace legacy Web group-proof entry with typed search."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
FILE = 'web_group_proof.py'
NEW = '''def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
) -> WebGroupProofView:
  """Search a typed group goal and render complete or partial proof evidence."""
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for positive-dimensional group queries")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")

  from phase165_r52_r5_auto_search import search_group_structure_automatically
  from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

  result = search_group_structure_automatically(n=n, k=k)
  return build_partial_web_group_proof_view(
    result,
    max_depth=max_depth,
    mode=mode,
  )
'''


def function_node(tree, name):
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f'Expected exactly one {name} in {FILE}')
    return matches[0]


def patch(source):
    tree = ast.parse(source)
    current = function_node(tree, 'build_standard_web_group_proof_view')
    desired = ast.parse(NEW).body[0]
    if ast.dump(current, include_attributes=False) == ast.dump(desired, include_attributes=False):
        return source, False
    old_names = {n.id for n in ast.walk(current) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    if ('build_standard_toda_report' not in old_names and
            'search_group_structure_automatically' not in old_names):
        raise RuntimeError('Unrecognized Web group-proof entry: refusing to overwrite')
    lines = source.splitlines(keepends=True)
    lines[current.lineno - 1:current.end_lineno] = [NEW]
    updated = ''.join(lines)
    # Remove only obsolete imports that are not used by any other source code.
    for name in ('build_standard_toda_report', 'TodaCalculationStatus'):
        t = ast.parse(updated)
        referencing = [n for n in ast.walk(t) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id == name]
        if referencing:
            continue
        imports = [n for n in t.body if isinstance(n, ast.ImportFrom) and len(n.names) == 1 and n.names[0].name == name]
        for node in reversed(imports):
            ls = updated.splitlines(keepends=True)
            ls[node.lineno - 1:node.end_lineno] = []
            updated = ''.join(ls)
    ast.parse(updated)
    return updated, True


def apply(root=ROOT):
    target = root / FILE
    if not target.is_file():
        raise FileNotFoundError(target)
    original = target.read_text(encoding='utf-8-sig')
    updated, changed = patch(original)
    if changed:
        backup = root / 'phase165_r27_r33_web_group_proof_backup.py.bak'
        if backup.exists() and backup.read_text(encoding='utf-8') != original:
            raise RuntimeError('Existing backup differs; refusing overwrite')
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_text(updated, encoding='utf-8')
        print('R27-R33 installed: Web Group Proof now uses common typed Backward Search')
    else:
        print('R27-R33 already installed')


if __name__ == '__main__':
    apply()
