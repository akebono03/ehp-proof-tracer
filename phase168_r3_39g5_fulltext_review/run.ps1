$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Project
try {
    python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_review.py')
    if ($LASTEXITCODE -ne 0) { throw 'Focused review tests failed' }
    python -m phase168_r3_39f_frozen_comparison.audit
    if ($LASTEXITCODE -ne 0) { throw 'Frozen comparison failed' }
    python (Join-Path $PSScriptRoot 'review.py')
    if ($LASTEXITCODE -ne 0) { throw 'Full-text review failed' }
    Write-Host 'R3-39G-5 review complete. No implementation changes. Full pytest NOT run.'
}
finally {
    Pop-Location
}
