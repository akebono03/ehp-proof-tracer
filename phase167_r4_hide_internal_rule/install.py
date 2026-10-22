from pathlib import Path
import ast
import sys
root=Path.cwd()
path=root/'toda_group_proof_narrative_shared_components.py'
source=path.read_text(encoding='utf-8-sig')
needle='  if proof_step.inference_rule is not None:\n    return proof_step.inference_rule.name'
replacement='  if proof_step.inference_rule is not None:\n    if proof_step.inference_rule.name == "infinite cyclic quotient structure":\n      return ""\n    return proof_step.inference_rule.name'
normal=source.replace('\r\n','\n')
if normal.count(needle)!=1:
    raise SystemExit('ABORT: expected exact current generic fallback not found; no changes')
updated=normal.replace(needle,replacement,1)
ast.parse(updated)
path.write_bytes(updated.replace('\n','\r\n').encode('utf-8') if '\r\n' in source else updated.encode('utf-8'))
print('PATCHED:',path.name,'_render_generic_narrative_step')
# replacement full function for audit
fn=next(n for n in ast.parse(updated).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=='_render_generic_narrative_step')
lines=updated.splitlines(keepends=True)
(root/'phase167_r4_hide_internal_rule'/'modified_function_full.py.txt').write_text(''.join(lines[fn.lineno-1:fn.end_lineno]),encoding='utf-8')
