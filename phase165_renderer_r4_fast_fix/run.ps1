$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { "$project$([IO.Path]::PathSeparator)$package" } else { "$project$([IO.Path]::PathSeparator)$package$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
$baseline = Join-Path $package 'baseline.json'
& $python (Join-Path $package 'snapshot.py') before $baseline
if ($LASTEXITCODE -ne 0) { throw 'Pre-install baseline failed; nothing changed' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R4 fast migration failed; inspect .phase165_renderer_r4_fast_backup' }
& $python -m pytest -q (Join-Path $package 'test_r4_fast.py') (Join-Path $project 'test_phase165_r52_r11_common_renderer.py') (Join-Path $project 'test_phase165_r56_common_renderer.py')
$code = $LASTEXITCODE
if ($code -eq 0) {
    & $python (Join-Path $package 'snapshot.py') after $baseline
    $code = $LASTEXITCODE
}
if ($code -ne 0) {
    Write-Output 'Regression detected; restoring R3 source'
    & $python (Join-Path $package 'restore.py')
    if ($LASTEXITCODE -ne 0) { throw 'R4 fast rollback failed; backup remains intact' }
    throw 'R4 fast regression, restored R3'
}
Write-Output 'R4 fast migration verified; Narrative parity passed; full pytest NOT run.'
