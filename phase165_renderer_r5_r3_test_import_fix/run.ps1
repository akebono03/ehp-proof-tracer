$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { "$project$([IO.Path]::PathSeparator)$package" } else { "$project$([IO.Path]::PathSeparator)$package$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 R3 test import patch failed. No further steps executed.' }
& $python -m pytest -q (Join-Path $package 'test_install.py') (Join-Path $project 'tests/test_phase162_r2_validated_proof_presentation.py') (Join-Path $project 'test_phase165_r56_common_renderer.py')
if ($LASTEXITCODE -ne 0) {
    Write-Output 'Targeted regression detected; restoring changed test.'
    & $python (Join-Path $package 'install.py') --restore
    if ($LASTEXITCODE -ne 0) { throw 'R5 R3 restore failed; inspect backup.' }
    throw 'R5 R3 targeted pytest failed; original test restored.'
}
& $python (Join-Path $project 'phase165_renderer_r5_r2_archive_classification/audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 static audit still failing; patched test retained, inspect audit report.' }
Write-Output 'R5 R3: two legacy test imports migrated; targeted pytest and static audit passed. Full pytest NOT run.'
