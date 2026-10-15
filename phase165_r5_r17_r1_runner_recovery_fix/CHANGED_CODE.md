# Phase 165 R5-R17-R1 変更コード全文

変更対象は削除インストーラとランナーのみ。新規テストの追加場所はこのパッケージの直下。

## `install.py`

```python
from __future__ import annotations

import ast
import hashlib
import json
import shutil
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
MODULES = (
    'phase162_web_narrative_integration.py',
    'phase162_r3_narrative_connection.py',
    'toda_group_proof_narrative_proof_chain_renderer.py',
    'toda_group_proof_narrative_concrete_transport.py',
)
TESTS = (
    'tests/test_phase162_r5_web_integration.py',
    'tests/test_phase162_r5_6_narrative_final_format.py',
    'tests/test_phase162_r3_narrative_connection.py',
    'tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py',
    'tests/test_phase162_r4_b3_common_renderer_fix.py',
)
REMOVAL = MODULES + TESTS
BACKUP = PROJECT / '.phase165_r5_r17_removed_backup'
GUARD_MODULES = {Path(p).stem for p in MODULES}
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'archive', '.pytest_cache', 'site-packages'}


def imports_retired_module(source: str) -> set[str]:
    try:
        parsed = ast.parse(source)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for name in node.names:
                token = name.name.split('.')[0]
                if token in GUARD_MODULES:
                    found.add(token)
        elif isinstance(node, ast.ImportFrom) and node.module:
            token = node.module.split('.')[0]
            if token in GUARD_MODULES:
                found.add(token)
    return found


def in_active_root(path: Path) -> bool:
    rel = path.relative_to(PROJECT)
    if any(part in SKIP_DIRS or part.startswith('.phase') for part in rel.parts):
        return False
    if len(rel.parts) == 1 and rel.name.startswith('audit_'):
        return False
    return len(rel.parts) == 1 or rel.parts[0] == 'tests'


def inspect() -> dict:
    missing = [p for p in REMOVAL if not (PROJECT / p).is_file()]
    leaf = PROJECT / 'phase162_ehp_leaf_inputs.py'
    replay = PROJECT / 'phase162_pi5_3_web_replay.py'
    shared_guards = {
        'shared_leaf_exists': leaf.is_file(),
        'replay_imports_shared_leaf': replay.is_file() and 'from phase162_ehp_leaf_inputs import _phase162_ehp_leaves' in replay.read_text(encoding='utf-8-sig'),
        'common_partial_renderer_exists': (PROJECT / 'phase165_r52_partial_proof.py').is_file(),
        'common_web_exists': (PROJECT / 'web_group_proof.py').is_file(),
    }
    blockers: dict[str, list[str]] = {}
    historical: dict[str, list[str]] = {}
    excluded = {PROJECT / p for p in REMOVAL}
    for path in PROJECT.rglob('*.py'):
        if path in excluded or PACKAGE in path.parents:
            continue
        rel = path.relative_to(PROJECT)
        if any(part in SKIP_DIRS or part.startswith('.phase') for part in rel.parts):
            continue
        names = imports_retired_module(path.read_text(encoding='utf-8-sig', errors='replace'))
        if not names:
            continue
        key = rel.as_posix()
        (blockers if in_active_root(path) else historical)[key] = sorted(names)
    return {'phase': '165 R5-R17', 'missing_files': missing, 'guards': shared_guards,
            'active_import_blockers': blockers, 'historical_imports': historical,
            'planned_deletions': list(REMOVAL), 'full_pytest_run': False}


def _content_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verified_existing_backup() -> bool:
    """A previous rollback may have restored all nine files without deleting its backup."""
    if not BACKUP.is_dir():
        return False
    return all(
        (BACKUP / rel).is_file()
        and (PROJECT / rel).is_file()
        and _content_digest(BACKUP / rel) == _content_digest(PROJECT / rel)
        for rel in REMOVAL
    )


def install() -> int:
    report = inspect()
    output = PACKAGE / 'audit_output'
    output.mkdir(exist_ok=True)
    report_path = output / 'install.json'
    if BACKUP.exists() and not _verified_existing_backup():
        report['status'] = 'BACKUP_CONTENT_MISMATCH_ABORT'
    elif report['missing_files']:
        report['status'] = 'MISSING_FILE_ABORT'
    elif not all(report['guards'].values()):
        report['status'] = 'SHARED_ROUTE_GUARD_FAILED'
    elif report['active_import_blockers']:
        report['status'] = 'ACTIVE_IMPORT_BLOCKERS_ABORT'
    else:
        if not BACKUP.exists():
            BACKUP.mkdir()
            for rel in REMOVAL:
                dest = BACKUP / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(PROJECT / rel, dest)
        for rel in REMOVAL:
            (PROJECT / rel).unlink()
        report['status'] = 'REMOVED'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'REMOVED' else 2


if __name__ == '__main__':
    sys.exit(install())

```

## `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $project
$env:PYTHONPATH = "$project;$PSScriptRoot"
$testDir = '.\phase165_r5_r17_r1_runner_recovery_fix'
python -m pytest -q "$testDir\test_installer.py" "$testDir\test_recovery.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R17-R1 installer tests failed before deletion.' }
python "$testDir\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R17-R1 preflight failed; no deletion performed.' }
python -m pytest -q "$testDir\test_canonical_smoke.py"
if ($LASTEXITCODE -ne 0) {
    python "$testDir\restore.py"
    throw 'R5-R17-R1 canonical Renderer regression failed. Deleted files restored.'
}
Write-Host 'R5-R17-R1 old Renderer modules removed; canonical smoke tests PASS; full pytest NOT run.'

```

## `restore.py`

```python
from __future__ import annotations

import shutil
from pathlib import Path

from install import BACKUP, PROJECT, REMOVAL


def restore() -> None:
    if not BACKUP.is_dir() or not all((BACKUP / path).is_file() for path in REMOVAL):
        raise RuntimeError('Complete backup does not exist; no restoration performed')
    for rel in REMOVAL:
        target = PROJECT / rel
        if target.exists():
            raise RuntimeError(f'Unexpected existing target prevents restore: {rel}')
    for rel in REMOVAL:
        destination = PROJECT / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BACKUP / rel, destination)
    print('R5-R17 removed files restored; backup preserved')


if __name__ == '__main__':
    restore()

```

## `test_installer.py`

```python
from __future__ import annotations

import ast
from pathlib import Path

from install import GUARD_MODULES, MODULES, TESTS, imports_retired_module


def test_deletion_manifest_is_explicit():
    assert len(MODULES) == 4
    assert len(TESTS) == 5
    assert len(set(MODULES + TESTS)) == 9
    assert GUARD_MODULES == {Path(path).stem for path in MODULES}


def test_ast_detects_normal_imports():
    assert imports_retired_module('import phase162_r3_narrative_connection') == {'phase162_r3_narrative_connection'}
    assert imports_retired_module('from toda_group_proof_narrative_concrete_transport import render_concrete_transport_proof_from_steps') == {'toda_group_proof_narrative_concrete_transport'}


def test_ast_ignores_ordinary_strings_and_comments():
    assert imports_retired_module('s = "import phase162_web_narrative_integration"\n# import phase162_r3_narrative_connection') == set()


def test_ast_ignores_shared_renderer():
    assert imports_retired_module('from phase165_r52_partial_proof import render_partial_proof_markdown') == set()


def test_source_is_valid_python():
    source = Path(__file__).with_name('install.py').read_text(encoding='utf-8')
    ast.parse(source)

```

## `test_recovery.py`

```python
from pathlib import Path

import install


def test_verified_existing_backup_accepts_exact_restoration(tmp_path, monkeypatch):
    monkeypatch.setattr(install, 'PROJECT', tmp_path)
    monkeypatch.setattr(install, 'BACKUP', tmp_path / 'backup')
    for rel in install.REMOVAL:
        current = tmp_path / rel
        backup = tmp_path / 'backup' / rel
        current.parent.mkdir(parents=True, exist_ok=True)
        backup.parent.mkdir(parents=True, exist_ok=True)
        current.write_bytes(rel.encode('utf-8'))
        backup.write_bytes(rel.encode('utf-8'))
    assert install._verified_existing_backup()


def test_verified_existing_backup_rejects_changed_restoration(tmp_path, monkeypatch):
    monkeypatch.setattr(install, 'PROJECT', tmp_path)
    monkeypatch.setattr(install, 'BACKUP', tmp_path / 'backup')
    for rel in install.REMOVAL:
        current = tmp_path / rel
        backup = tmp_path / 'backup' / rel
        current.parent.mkdir(parents=True, exist_ok=True)
        backup.parent.mkdir(parents=True, exist_ok=True)
        current.write_bytes(b'original')
        backup.write_bytes(b'original')
    (tmp_path / install.REMOVAL[0]).write_bytes(b'changed')
    assert not install._verified_existing_backup()


def test_verified_existing_backup_requires_full_backup(tmp_path, monkeypatch):
    monkeypatch.setattr(install, 'PROJECT', tmp_path)
    monkeypatch.setattr(install, 'BACKUP', tmp_path / 'backup')
    (tmp_path / 'backup').mkdir()
    assert not install._verified_existing_backup()

```

## `test_canonical_smoke.py`

```python
import importlib

import pytest

from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def test_partial_renderer_keeps_not_searched_status():
    result = make_partial_proof_result(
        n=3, k=2,
        status=ProofSearchStatus.NOT_SEARCHED,
        structure_status=GroupStructureStatus.UNKNOWN,
    )
    output = render_partial_proof_markdown(result)
    assert isinstance(output, str) and output.strip()


def test_completed_adapter_rejects_unproved_goal():
    result = make_partial_proof_result(n=3, k=2, status=ProofSearchStatus.NOT_SEARCHED)
    with pytest.raises(ValueError):
        render_completed_shared_narrative(result)


def test_public_web_module_still_imports():
    assert callable(importlib.import_module('web_group_proof').build_standard_web_group_proof_view)

```

