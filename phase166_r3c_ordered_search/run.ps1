$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Project
try {
    $env:PYTHONPATH = $Project
    python '.\phase166_r3c_ordered_search\install.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C install failed' }
    python -m pytest -q '.\phase166_r3c_ordered_search\tests\test_phase166_r3c_ordered_search.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C targeted tests failed' }
    Write-Host 'Phase 166 R3-C targeted PASS; full pytest NOT run.'
} finally { Pop-Location }
