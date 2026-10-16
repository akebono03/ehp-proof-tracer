$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $Root + [IO.Path]::PathSeparator + $oldPythonPath
    python -m pytest -q (Join-Path $PSScriptRoot "test_phase165_r6_2_r2_verified_inverse.py")
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
} finally {
    $env:PYTHONPATH = $oldPythonPath
}
Write-Host "R6-2 R2 verified witness inverse tests complete. Full pytest NOT run."
