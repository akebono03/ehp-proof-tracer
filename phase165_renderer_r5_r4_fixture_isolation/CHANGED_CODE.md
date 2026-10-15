# R5-R4 変更コード全文

## インストーラー（全文）

```python
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

OLD = "from toda_group_proof_generic_narrative_renderer import (\n        _render_generic_narrative_step,\n    )"
NEW = "from toda_group_proof_narrative_renderer import (\n        _render_generic_narrative_step,\n    )"
TARGET = Path("tests/test_phase162_r2_validated_proof_presentation.py")
BACKUP = Path(".phase165_renderer_r5_r3_test_backup/test_phase162_r2_validated_proof_presentation.py")

def install(project: Path) -> dict:
    path = project / TARGET
    backup = project / BACKUP
    if not path.is_file():
        raise FileNotFoundError(str(path))
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    text = data.decode("utf-8-sig")
    normalized = text.replace("\r\n", "\n")
    if normalized.count(NEW) == 2 and normalized.count(OLD) == 0:
        return {"status": "ALREADY_INSTALLED", "changed_file": str(TARGET), "import_sites": 2}
    if normalized.count(OLD) != 2:
        raise RuntimeError("Unexpected imports in target test; no changes made: " + str(normalized.count(OLD)))
    modified = normalized.replace(OLD, NEW)
    ast.parse(modified)
    if len([n for n in ast.walk(ast.parse(modified)) if isinstance(n, ast.ImportFrom) and n.module == 'toda_group_proof_generic_narrative_renderer']) != 0:
        raise RuntimeError('Unmigrated old imports: no changes made')
    if backup.exists():
        if backup.read_bytes() != data:
            raise RuntimeError('Backup already exists with different content; no changes made')
    else:
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    linebreak = "\r\n" if b"\r\n" in data else "\n"
    output = (b"\xef\xbb\xbf" if bom else b"") + modified.replace("\n", linebreak).encode("utf-8")
    path.write_bytes(output)
    return {"status": "INSTALLED", "changed_file": str(TARGET), "import_sites": 2, "backup": str(BACKUP)}

def restore(project: Path) -> dict:
    backup = project / BACKUP
    destination = project / TARGET
    if not backup.is_file():
        raise FileNotFoundError(str(backup))
    shutil.copy2(backup, destination)
    return {"status": "RESTORED", "path": str(TARGET)}

if __name__ == '__main__':
    import sys
    project = Path(__file__).resolve().parent.parent
    result = restore(project) if len(sys.argv) > 1 and sys.argv[1] == '--restore' else install(project)
    print(json.dumps(result, ensure_ascii=False, indent=2))

```

## 限定テスト（全文）

```python
from pathlib import Path
import ast
import pytest
from install import OLD, NEW, TARGET, BACKUP, install, restore

def test_exact_two_legacy_imports_are_replaced(tmp_path: Path) -> None:
    p = tmp_path / TARGET
    p.parent.mkdir(parents=True)
    p.write_text('def a():\n    ' + OLD + '\ndef b():\n    ' + OLD + '\n', encoding='utf-8')
    report = install(tmp_path)
    assert report['status'] == 'INSTALLED'
    assert p.read_text(encoding='utf-8').count(NEW) == 2
    assert not any(isinstance(n, ast.ImportFrom) and n.module == 'toda_group_proof_generic_narrative_renderer' for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))))
    assert restore(tmp_path)['status'] == 'RESTORED'
    assert p.read_text(encoding='utf-8').count(OLD) == 2

def test_refuse_any_different_import_shape(tmp_path: Path) -> None:
    p = tmp_path / TARGET
    p.parent.mkdir(parents=True)
    p.write_text('x = 1\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='Unexpected imports'):
        install(tmp_path)
    assert p.read_text(encoding='utf-8') == 'x = 1\n'
    assert not (tmp_path / BACKUP).exists()

def test_bom_is_preserved_and_reinstall_is_safe(tmp_path: Path) -> None:
    p = tmp_path / TARGET
    p.parent.mkdir(parents=True)
    data = ('def a():\n    ' + OLD + '\ndef b():\n    ' + OLD + '\n').encode('utf-8')
    p.write_bytes(b'\xef\xbb\xbf'+data)
    assert install(tmp_path)['status']=='INSTALLED'
    assert p.read_bytes().startswith(b'\xef\xbb\xbf')
    assert install(tmp_path)['status']=='ALREADY_INSTALLED'
    assert restore(tmp_path)['status']=='RESTORED'
    assert p.read_bytes()==b'\xef\xbb\xbf'+data

```

## PowerShell ランナー（全文）

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { "$project$([IO.Path]::PathSeparator)$package" } else { "$project$([IO.Path]::PathSeparator)$package$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 R4 import migration failed; unchanged if preflight failed.' }
& $python -m pytest -q (Join-Path $package 'test_install.py') (Join-Path $project 'test_phase165_r56_common_renderer.py') (Join-Path $project 'test_phase165_r52_r11_common_renderer.py')
if ($LASTEXITCODE -ne 0) {
    Write-Output 'Relevant scoped tests failed; restoring modified import test.'
    & $python (Join-Path $package 'install.py') --restore
    if ($LASTEXITCODE -ne 0) { throw 'Restore failed; inspect existing .phase165_renderer_r5_r3_test_backup.' }
    throw 'R5 R4 scoped regression; old imports restored.'
}
& $python (Join-Path $project 'phase165_renderer_r5_r2_archive_classification/audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 active-import static check still fails; migration retained; inspect report.' }
Write-Output 'R5 R4 scoped tests and active-import audit passed. Historical Phase162 fixture tests remain UNRESOLVED (6 failures from empty prop51_steps). Full pytest NOT run.'

```

## 置換対象となる既存 import（2か所とも同一）

```python
from toda_group_proof_narrative_renderer import (
    _render_generic_narrative_step,
)
```
