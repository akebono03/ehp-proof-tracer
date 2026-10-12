"""Restore only R8-R6 files from the backup directory named in its report."""
import json
from pathlib import Path

root=Path.cwd()
audit=json.loads((root/'phase164_r8_r6_output/audit.json').read_text(encoding='utf-8'))
backup=Path(audit['backup_dir'])
for name in audit['changed_files']:
    data=(backup/name).read_bytes()
    (root/name).write_bytes(data)
    print('Restored:',name)
