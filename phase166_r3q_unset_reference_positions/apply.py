"""Apply the reviewed Proposition 4.2 source-ID mapping only."""
from __future__ import annotations
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase166_r3l_reference_order.py'
OLD = '''    "typed_literature:toda:tex:ch5:0003": "toda:(5.2)",\n'''
NEW = '''    "typed_literature:toda:tex:ch5:0003": "toda:(5.2)",
    "adopted:ref:7": "toda:Proposition 4.2",
    "adopted:ref:8": "toda:Proposition 4.2",
    "adopted:ref:9": "toda:Proposition 4.2",
    "adopted:reference:prop42:general": "toda:Proposition 4.2",
'''

def main():
    source = TARGET.read_text(encoding='utf-8')
    if OLD not in source or source.count(OLD) != 1:
        raise RuntimeError('Expected alias insertion anchor not found uniquely; nothing changed')
    if '"adopted:ref:7": "toda:Proposition 4.2"' in source:
        raise RuntimeError('Already applied; nothing changed')
    revised = source.replace(OLD, NEW, 1)
    ast.parse(revised, filename=str(TARGET))
    backup_dir = ROOT / 'phase166_r3q_unset_reference_positions_backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup = backup_dir / TARGET.name
    backup.write_text(source, encoding='utf-8')
    TARGET.write_text(revised, encoding='utf-8')
    state = {'target': str(TARGET), 'backup': str(backup), 'original_sha256': hashlib.sha256(source.encode()).hexdigest(), 'patched_sha256': hashlib.sha256(revised.encode()).hexdigest()}
    (Path(__file__).parent / 'last_install.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
    print('PATCHED:', TARGET)
    print('BACKUP:', backup)
    print('CHANGED: REVIEWED_REFERENCE_ALIASES (4 entries only)')

if __name__ == '__main__':
    main()
