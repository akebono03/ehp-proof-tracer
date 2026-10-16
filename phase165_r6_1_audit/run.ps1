$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
Set-Location $Root
$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $Package + [IO.Path]::PathSeparator + $Root
    python -m pytest -q (Join-Path $Package 'test_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R6-1 audit tests failed' }
    python (Join-Path $Package 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R6-1 audit failed' }
} finally {
    $env:PYTHONPATH = $OldPythonPath
}
Write-Host 'Phase 165 R6-1 audit completed (read-only). Full pytest NOT run.'
