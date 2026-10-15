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
