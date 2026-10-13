"""Guarded correction for the existing Phase 165 R9 Goal-only entry contract."""
import ast
from pathlib import Path

root = Path.cwd()
package = Path(__file__).resolve().parent
entry = root / 'phase165_goal_only_search.py'
if not entry.is_file():
    raise SystemExit('Missing phase165_goal_only_search.py; run from the repository root')
source = entry.read_text(encoding='utf-8')
tree = ast.parse(source)
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'construct_registered_group_proof']
if len(functions) != 1:
    raise SystemExit('Expected exactly one construct_registered_group_proof function')
node = functions[0]
lines = source.splitlines(keepends=True)
old = ''.join(lines[node.lineno - 1:node.end_lineno])
required = ('legacy proof selection remains disabled', 'reconstruct_registered_goal(', 'GoalSearchIncompleteError', 'verified_assertion_ids=verified_assertion_ids')
replacement = (package / 'construct_registered_group_proof.py.txt').read_text(encoding='utf-8').rstrip('\n') + '\n'
if old.strip() == replacement.strip():
    print('R52-R2 Goal-only entry correction already installed')
elif all(x in old for x in required) and 'discover_goal_search_inputs' not in old:
    lines[node.lineno - 1:node.end_lineno] = [replacement]
    candidate = ''.join(lines)
    ast.parse(candidate)
    entry.write_text(candidate, encoding='utf-8')
    print('Corrected Goal-only production discovery and failure message')
else:
    raise SystemExit('Goal-only entry differs from audited version; refusing overwrite')
