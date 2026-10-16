$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root
$OldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$Root" + [IO.Path]::PathSeparator + $OldPythonPath
    python (Join-Path $PSScriptRoot "apply.py")
    if ($LASTEXITCODE -ne 0) { throw "R6-2 R4 installation failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "test_r624.py")
    if ($LASTEXITCODE -ne 0) { throw "R6-2 R4 focused tests failed" }
    Write-Host "R6-2 R4 seeded premise goals connected. Full pytest NOT run."
} finally {
    $env:PYTHONPATH = $OldPythonPath
}
