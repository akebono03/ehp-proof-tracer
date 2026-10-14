"""Apply the narrowly scoped R27-R13 file-count correction."""
from pathlib import Path

root = Path.cwd()
target = root / 'phase165_r27_r13' / 'audit.py'
if not target.is_file():
    raise SystemExit('R27-R13 audit.py not found; no files changed')
old = "files=dict(sorted(Counter(e['scope'] for e in { (x['path'],x['scope']) for x in entries} for _ in [0]).items()))"
new = "files=dict(sorted(Counter(scope for path, scope in {(x['path'], x['scope']) for x in entries}).items()))"
content = target.read_text(encoding='utf-8')
if new in content and old not in content:
    print('R27-R13 file-count correction already applied')
elif content.count(old) == 1:
    target.write_text(content.replace(old, new), encoding='utf-8')
    print('Updated: phase165_r27_r13/audit.py (distinct file count by scope)')
else:
    raise SystemExit('Unexpected audit.py content; refusing to modify')
