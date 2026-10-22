"""Replace precisely the existing citation resolver, retaining a backup."""
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
target = root / 'phase166_r3t_goal_source_binding' / 'goal_source.py'
replacement = (Path(__file__).parent / 'replacement_function.py').read_text(encoding='utf-8').rstrip()
source = target.read_text(encoding='utf-8')
tree = ast.parse(source)
matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'resolve_specialized_goal_citing_id']
if len(matches) != 1:
    raise RuntimeError('Expected exactly one citation resolver')
old = matches[0]
lines = source.splitlines(keepends=True)
updated = ''.join(lines[:old.lineno-1]) + replacement + '\n' + ''.join(lines[old.end_lineno:])
ast.parse(updated)
if updated == source:
    print('ALREADY_APPLIED:', target)
else:
    backup = root / 'phase168_r2_8_4_backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup / 'goal_source.py')
    target.write_text(updated, encoding='utf-8')
    print('PATCHED:', target)
    print('BACKUP:', backup / 'goal_source.py')
print('FULL_FUNCTION:', Path(__file__).parent / 'replacement_function.py')
