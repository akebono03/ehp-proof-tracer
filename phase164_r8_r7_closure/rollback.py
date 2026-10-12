"""Restore only the latest R8-R7 backups, without touching earlier phases."""
from pathlib import Path
import json

root = Path.cwd()
report = json.loads((root / 'phase164_r8_r7_output' / 'audit.json').read_text(encoding='utf-8'))
backup = Path(report['backup_dir'])
for filename in report['changed_files']:
    source = backup / filename
    if not source.is_file():
        raise FileNotFoundError(source)
    (root / filename).write_bytes(source.read_bytes())
print('R8-R7 changes restored from', backup)
