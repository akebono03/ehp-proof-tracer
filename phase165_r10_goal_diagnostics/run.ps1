$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Source = Join-Path $PSScriptRoot 'phase165_r10_goal_diagnostics.py'
$Target = Join-Path $Root 'phase165_r10_goal_diagnostics.py'
$TestSource = Join-Path (Join-Path $PSScriptRoot 'tests') 'test_phase165_r10_goal_diagnostics.py'
$TestTarget = Join-Path (Join-Path $Root 'tests') 'test_phase165_r10_goal_diagnostics.py'
foreach ($file in @($Source, $TestSource)) { if (-not (Test-Path $file)) { throw "Missing package file: $file" } }
if (Test-Path $Target) { Copy-Item $Target "$Target.phase165_r10_backup" -Force }
if (Test-Path $TestTarget) { Copy-Item $TestTarget "$TestTarget.phase165_r10_backup" -Force }
Copy-Item $Source $Target -Force
Copy-Item $TestSource $TestTarget -Force
python -m py_compile $Target $TestTarget
if ($LASTEXITCODE -ne 0) { throw 'Syntax validation failed' }
python -m pytest -q 'tests/test_phase165_r10_goal_diagnostics.py' 'tests/test_phase165_r9_production_wiring.py'
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$OldPythonPath"
    python (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10 audit failed' }
} finally { $env:PYTHONPATH = $OldPythonPath }
Write-Host 'R10 focused tests and production diagnostic audit finished; full pytest NOT run.'
