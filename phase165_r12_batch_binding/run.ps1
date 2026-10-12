$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Source = Join-Path $PSScriptRoot 'phase165_r12_typed_binding.py'
$TestSource = Join-Path $PSScriptRoot 'tests/test_phase165_r12_typed_binding.py'
$Target = Join-Path $Root 'phase165_r12_typed_binding.py'
$TestTarget = Join-Path $Root 'tests/test_phase165_r12_typed_binding.py'
foreach ($Path in @($Source, $TestSource)) {
    if (-not (Test-Path $Path)) { throw "Missing package file: $Path" }
}
if (Test-Path $Target) { Copy-Item $Target "$Target.phase165_r12_backup" -Force }
if (Test-Path $TestTarget) { Copy-Item $TestTarget "$TestTarget.phase165_r12_backup" -Force }
Copy-Item $Source $Target -Force
Copy-Item $TestSource $TestTarget -Force
python -m py_compile $Target $TestTarget
if ($LASTEXITCODE -ne 0) { throw 'R12 Python syntax failed' }
python -m pytest -q $TestTarget
if ($LASTEXITCODE -ne 0) { throw 'R12 focused tests failed' }
$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$OldPythonPath"
    python (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R12 audit failed' }
} finally {
    $env:PYTHONPATH = $OldPythonPath
}
Write-Host 'R12 batch source bindings completed. No typed mathematical theorem automatically approved. Full pytest NOT run.'
