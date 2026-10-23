$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Push-Location $repo
try {
    python (Join-Path $package 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
    $env:PYTHONPATH = "$package;$repo;$env:PYTHONPATH"
    python -m pytest -q (Join-Path $package 'tests\test_r3_30_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Limited audit tests failed' }
    Write-Host "R3-30 audit only: full pytest NOT run; repository unchanged."
} finally { Pop-Location }
