"""Apply the conservative R3-AF candidate fallback after preflight."""
from pathlib import Path
import ast
import shutil
from datetime import datetime, timezone

project=Path.cwd()
target=project/'phase165_r55_nk_only_goal.py'
original=target.read_text(encoding='utf-8')
tree=ast.parse(original)
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='registered_group_goal_candidates']
if len(funcs)!=2:
    raise SystemExit('STOP: expected exactly two existing candidate functions')
node=funcs[-1]
lines=original.splitlines(keepends=True)
old=''.join(lines[node.lineno-1:node.end_lineno])
if '_phase165_r57_r8_previous_registered_group_goal_candidates' not in old or 'specialized_eta_group_goal_candidates' not in old:
    raise SystemExit('STOP: unexpected candidate wrapper')
new='def registered_group_goal_candidates(bridge, *, n: int, k: int):\n    """Keep literature goals first; add database-derived targets only as goals."""\n    from homotopy_groups import TodaPrimaryGroup\n    from phase165_r57_r8_eta_specialization import specialized_eta_group_goal_candidates\n    from phase166_r3af_goal_adapter import database_group_goal_candidates\n\n    existing = _phase165_r57_r8_previous_registered_group_goal_candidates(bridge=bridge, n=n, k=k)\n    if not isinstance(existing, tuple):\n        raise TypeError("R55 selector must return a tuple")\n    group = TodaPrimaryGroup(group_dimension=n+k, sphere_dimension=n)\n    symbolic = specialized_eta_group_goal_candidates(group, bridge)\n    output = list(existing)\n    for candidate in symbolic:\n        if not any(type(candidate) is type(old) and candidate == old for old in output):\n            output.append(candidate)\n    if not output:\n        for candidate in database_group_goal_candidates(n=n, k=k):\n            if candidate not in output:\n                output.append(candidate)\n    return tuple(output)\n'
if old.strip()==new.strip():
    print('ALREADY_APPLIED')
else:
    backup=project/'phase166_r3af_backups'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup.mkdir(parents=True,exist_ok=True)
    shutil.copy2(target, backup/target.name)
    updated=''.join(lines[:node.lineno-1])+new+''.join(lines[node.end_lineno:])
    ast.parse(updated)
    target.write_text(updated,encoding='utf-8')
    print('PATCHED:',target)
    print('BACKUP:',backup)
    (project/'phase166_r3af_goal_source'/'modified_full_function.txt').write_text(new,encoding='utf-8')
shutil.copy2(project/'phase166_r3af_goal_source'/'phase166_r3af_goal_adapter.py',project/'phase166_r3af_goal_adapter.py')
print('INSTALLED: phase166_r3af_goal_adapter.py')
