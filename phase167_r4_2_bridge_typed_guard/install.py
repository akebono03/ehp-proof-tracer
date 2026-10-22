from pathlib import Path
import ast
import sys

root=Path(__file__).resolve().parent.parent
p=root/'toda_group_proof_narrative_contribution_renderer.py'
s=p.read_text(encoding='utf-8')
tree=ast.parse(s)
fn=next(x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name=='insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges')
lines=s.splitlines(keepends=True)
segment=''.join(lines[fn.lineno-1:fn.end_lineno])
needle='''      bridge = (\n        "$"\n        + render_toda_expression_latex('''
assert segment.count(needle)==1, 'Unexpected bridge implementation; no changes applied'
insert='''      # R4-2: a separately displayed, typed generator suspension already\n      # proves this bridge. Do not add a second mathematical statement.\n      # Compare structured generator identities, not rendered LaTeX or names.\n      from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension\n      from homotopy_groups import TodaSuspensionMap\n\n      def same_generator(left, right):\n        return (\n          left.generator is not None\n          and right.generator is not None\n          and left.generator == right.generator\n          and left.dimension == right.dimension\n          and left.source == right.source\n          and left.target == right.target\n        )\n\n      typed_suspension = consumer_step.conclusion\n      if (\n        isinstance(typed_suspension, GeneratorSuspension)\n        and isinstance(typed_suspension.map, TodaSuspensionMap)\n        and same_generator(typed_suspension.source_generator, lower.element)\n        and same_generator(typed_suspension.target_generator, upper.element)\n      ):\n        continue\n\n'''
segment2=segment.replace(needle,insert+needle)
assert segment!=segment2
changed=''.join(lines[:fn.lineno-1])+segment2+''.join(lines[fn.end_lineno:])
ast.parse(changed)
p.write_text(changed,encoding='utf-8')
newfn=next(x for x in ast.parse(changed).body if isinstance(x,ast.FunctionDef) and x.name==fn.name)
(root/'phase167_r4_2_bridge_typed_guard'/'modified_function_full.py.txt').write_text(''.join(changed.splitlines(keepends=True)[newfn.lineno-1:newfn.end_lineno]),encoding='utf-8')
print('PATCHED:',p)
print('FULL FUNCTION:',root/'phase167_r4_2_bridge_typed_guard'/'modified_function_full.py.txt')
