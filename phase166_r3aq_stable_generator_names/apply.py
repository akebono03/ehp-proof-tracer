from pathlib import Path
import ast
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
folder = Path(__file__).resolve().parent
target = root / 'phase166_r3aj_structured_generator.py'
replacement = (folder / 'replacement.py.txt').read_text(encoding='utf-8')
if not target.exists():
    raise SystemExit(f'MISSING: {target}')
source = target.read_text(encoding='utf-8')
start = source.find('def _base_element(')
end = source.find('\ndef structured_generator_from_ids(', start)
if start < 0 or end < 0:
    raise SystemExit('Unexpected module structure; no modifications made')
old = source[start:end]
if 'kinds' not in old or 'IteratedSuspension' not in old:
    raise SystemExit('Unexpected function body; no modifications made')
updated = source[:start] + replacement + source[end:]
ast.parse(updated)
backup = root / 'phase166_r3aq_stable_generator_names_backup' / target.name
backup.parent.mkdir(exist_ok=True)
shutil.copy2(target, backup)
target.write_text(updated, encoding='utf-8')
print('PATCHED:', target)
print('BACKUP:', backup)
print('FULL FUNCTION:', folder / 'replacement.py.txt')
