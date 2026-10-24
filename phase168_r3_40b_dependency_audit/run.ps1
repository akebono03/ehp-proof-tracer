$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Project
try {
    python -m pytest -q (Join-Path $PSScriptRoot 'tests\test_phase168_r3_40b_dependency_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Focused audit tests failed' }

    python (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Read-only dependency audit failed' }

    Write-Host 'R3-40B read-only audit complete. No implementation patch applied.'
    Write-Host 'Full pytest NOT run.'
}
finally {
    Pop-Location
}
