"""Restore only the files changed by R8-R5 from its recorded backup."""
from pathlib import Path
import json

root = Path.cwd()
report_path = root / 'phase164_r8_r5_output' / 'audit.json'
report = json.loads(report_path.read_text(encoding='utf-8'))
backup = Path(report['backup_dir'])
if not backup.is_dir() or backup.parent != root:
    raise ValueError('R8-R5 backup directory missing or unexpected')
files = list(backup.rglob('*.py'))
for file in files:
    target = root / file.relative_to(backup)
    target.write_bytes(file.read_bytes())
print(f'R8-R5 rollback restored {len(files)} files from {backup}')
