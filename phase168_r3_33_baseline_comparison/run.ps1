$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q (Join-Path $package 'tests\test_phase168_r3_33_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-33 focused tests failed' }
    python (Join-Path $package 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-33 audit failed; inspect output' }
    Write-Host 'R3-33 AUDIT_ONLY: source files unchanged; full pytest NOT run.'
}
finally { Pop-Location }
