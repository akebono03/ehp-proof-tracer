from __future__ import annotations

import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys

LEGACY = ('probes/probe_phase49_capabilities.py', 'probes/probe_phase56_capabilities.py')
CONSUMER = 'probes/probe_phase58_capabilities.py'
OLD_IMPORT = 'from probes.probe_phase49_capabilities import (\n  print_separator,\n)\n'
NEW_HELPER = 'def print_separator():\n  print("=" * 72)\n\n\n'


def active_sources(root: Path):
    yield from sorted(root.glob('*.py'))
    for folder in ('tests', 'probes'):
        d = root / folder
        if d.exists():
            yield from sorted(d.rglob('*.py'))


def dependencies(root: Path):
    blocked = []
    old_modules = {'probes.probe_phase49_capabilities', 'probes.probe_phase56_capabilities'}
    excluded = {root / x for x in LEGACY}
    consumer = root / CONSUMER
    for path in active_sources(root):
        if path in excluded or path == consumer:
            continue
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in old_modules:
                blocked.append({'path': path.relative_to(root).as_posix(), 'line': node.lineno, 'module': node.module})
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in old_modules:
                        blocked.append({'path': path.relative_to(root).as_posix(), 'line': node.lineno, 'module': alias.name})
    return blocked


def prepare_consumer(source: str):
    if source.count(OLD_IMPORT) != 1:
        raise ValueError('Unexpected Phase58 import; no changes applied')
    changed = source.replace(OLD_IMPORT, '', 1)
    tree = ast.parse(changed)
    if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'print_separator' for n in tree.body):
        raise ValueError('Local print_separator already exists')
    # Insert directly before the existing build function, without touching its body.
    anchor = '\ndef build_phase58_representative_result():'
    if changed.count(anchor) != 1:
        raise ValueError('Phase58 builder anchor not unique')
    changed = changed.replace(anchor, '\n' + NEW_HELPER + 'def build_phase58_representative_result():', 1)
    ast.parse(changed)
    return changed


def run(root: Path):
    paths = [root / x for x in (*LEGACY, CONSUMER)]
    if not all(p.is_file() for p in paths):
        raise RuntimeError('Required source missing; no changes made')
    blocked = dependencies(root)
    if blocked:
        raise RuntimeError('External legacy imports remain: ' + json.dumps(blocked, ensure_ascii=False))
    before = (root / CONSUMER).read_text(encoding='utf-8')
    after = prepare_consumer(before)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = root / 'phase165_r6_audit_results' / 'r6_13_probe_retirement' / ('backup_' + stamp)
    if backup.exists():
        raise RuntimeError('Backup destination already exists')
    manifest = []
    for path in paths:
        data = path.read_bytes()
        manifest.append({'path': str(path.relative_to(root)).replace('\\', '/'), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    for path in paths:
        dst = backup / path.relative_to(root)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
        if hashlib.sha256(dst.read_bytes()).hexdigest() != hashlib.sha256(path.read_bytes()).hexdigest():
            raise RuntimeError('Backup checksum mismatch: ' + str(path))
    (backup / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    changed = False
    try:
        (root / CONSUMER).write_text(after, encoding='utf-8')
        changed = True
        for relative in LEGACY:
            (root / relative).unlink()
        cmd = [sys.executable, '-c', 'import probes.probe_phase58_capabilities; from probes.probe_phase58_capabilities import print_separator; assert callable(print_separator)']
        subprocess.run(cmd, cwd=root, check=True, timeout=60)
        remaining = dependencies(root)
        if remaining:
            raise RuntimeError('Unexpected remaining imports: ' + str(remaining))
    except Exception:
        if changed:
            for path in paths:
                shutil.copy2(backup / path.relative_to(root), path)
        raise
    return {'phase': '165 R6-13', 'status': 'RETIRED_PROBES', 'retired': list(LEGACY), 'consumer_updated': CONSUMER, 'backup': str(backup), 'full_pytest_run': False}


if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    print(json.dumps(run(root), ensure_ascii=False, indent=2))
