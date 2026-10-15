"""Recover from an interrupted Phase165 Renderer R4 install; keep original backup."""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

BACKUP_NAME = '.phase165_renderer_r4_backup'
ALIAS_NAME = 'toda_group_proof_generic_narrative_renderer'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def restore(project: Path) -> dict:
    project = project.resolve()
    backup = project / BACKUP_NAME
    manifest_file = backup / 'manifest.json'
    if not manifest_file.is_file():
        raise RuntimeError('Backup manifest missing: NO FILES MODIFIED by recovery. Do not run R4 again.')
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    names = manifest.get('modified')
    if not isinstance(names, list) or not names or not all(isinstance(n, str) for n in names):
        raise RuntimeError('Invalid backup manifest: no changes made.')
    files = []
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or str(relative).startswith('.'):
            raise RuntimeError('Unsafe path in backup manifest: ' + name)
        original = backup / relative
        destination = project / relative
        if not original.is_file():
            raise RuntimeError('Missing original backup: ' + str(original))
        if original.suffix == '.py':
            ast.parse(original.read_text(encoding='utf-8'), filename=str(original))
        files.append((original, destination))
    alias_backup = backup / ALIAS_NAME
    if not (alias_backup / '__init__.py').is_file():
        raise RuntimeError('Original compatibility package missing from backup; no changes made.')
    alias_target = project / ALIAS_NAME
    required_restore = sum(not dst.is_file() or digest(src) != digest(dst) for src, dst in files)
    print(json.dumps({'stage':'VERIFIED_BACKUPS', 'files_in_manifest':len(files),
                      'files_needing_restore': required_restore,
                      'compatibility_package_present':alias_target.is_dir()},ensure_ascii=False),flush=True)
    restored = 0
    for src, dst in files:
        if dst.is_file() and digest(src) == digest(dst):
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_name(dst.name + '.r4_recovery_tmp')
        shutil.copy2(src, tmp)
        if digest(src) != digest(tmp):
            raise RuntimeError('Staged copy checksum mismatch: ' + str(dst))
        os.replace(tmp, dst)
        restored += 1
    alias_was_restored = False
    needs_alias = not alias_target.is_dir() or any(
        not (alias_target / p.relative_to(alias_backup)).is_file()
        or digest(p) != digest(alias_target / p.relative_to(alias_backup))
        for p in alias_backup.rglob('*') if p.is_file() and '__pycache__' not in p.parts
    )
    if needs_alias:
        stage = project / (ALIAS_NAME + '.r4_recovery_stage')
        if stage.exists():
            shutil.rmtree(stage)
        shutil.copytree(alias_backup, stage, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        if alias_target.exists():
            shutil.rmtree(alias_target)
        stage.rename(alias_target)
        alias_was_restored = True
    incorrect = [str(dst) for src, dst in files if not dst.is_file() or digest(src) != digest(dst)]
    if incorrect or not (alias_target/'__init__.py').is_file():
        raise RuntimeError('Verification failed: ' + ', '.join(incorrect))
    primary = project/'toda_group_proof_narrative_renderer.py'
    defs = [node for node in ast.parse(primary.read_text(encoding='utf-8')).body
            if isinstance(node, ast.FunctionDef) and node.name == 'render_toda_group_proof_narrative_markdown']
    if len(defs) != 2:
        raise RuntimeError('Unexpected R3 public definition count after restore: ' + str(len(defs)))
    return {'status':'RESTORED_R3', 'files_restored':restored,
            'alias_restored':alias_was_restored, 'original_backup_preserved':str(backup),
            'canonical_public_defs':len(defs), 'full_pytest_run':False}


if __name__ == '__main__':
    project = Path(__file__).resolve().parent.parent
    try:
        print(json.dumps(restore(project),ensure_ascii=False,indent=2),flush=True)
    except Exception as exc:
        print('RECOVERY_FAILED: '+str(exc),file=sys.stderr,flush=True)
        sys.exit(1)
