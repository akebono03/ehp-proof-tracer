from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
path = root / 'toda_group_proof_narrative_references.py'
source = path.read_text(encoding='utf-8')
tree = ast.parse(source)
name = 'render_toda_group_proof_narrative_reference_entries_markdown'
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
if len(nodes) != 1:
    raise RuntimeError('expected exactly one reference renderer')
node = nodes[0]
lines = source.splitlines(keepends=True)
function = ''.join(lines[node.lineno - 1:node.end_lineno])
old_ge = 'component.range_text.replace(">=", r"\\ge ")'
old_le = '.replace("<=", r"\\le ")'
new_ge = 'component.range_text.replace(">=", r"\\ge")'
new_le = '.replace("<=", r"\\le")'
if old_ge in function and old_le in function:
    changed = function.replace(old_ge, new_ge).replace(old_le, new_le)
    lines[node.lineno - 1:node.end_lineno] = [changed]
    result = ''.join(lines)
    ast.parse(result)
    path.write_text(result, encoding='utf-8')
    print('Updated: ' + str(path))
elif new_ge in function and new_le in function:
    print('Already applied: ' + str(path))
else:
    raise RuntimeError('Unexpected renderer implementation: no changes applied')
