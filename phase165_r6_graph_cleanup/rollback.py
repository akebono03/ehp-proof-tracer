"""Restore one graph cleanup session without overwriting existing files."""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, type=Path)
    ap.add_argument('--session', required=True, type=Path)
    args = ap.parse_args()
    root, session = args.root.resolve(), args.session.resolve()
    report = json.loads((session/'report.json').read_text(encoding='utf-8'))
    selected = [r for r in report['decisions'] if r['decision'] == 'REMOVE']
    for r in selected:
        src = session/'backup'/r['path']
        dst = root/r['path']
        if dst.exists() or not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest() != r['sha256']:
            raise RuntimeError('Cannot restore safely: ' + r['path'])
    for r in selected:
        src, dst = session/'backup'/r['path'], root/r['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print('Restored:', len(selected))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
