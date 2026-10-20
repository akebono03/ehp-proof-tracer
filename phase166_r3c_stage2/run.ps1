$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python '.\phase166_r3c_stage2\install.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C stage 2 install failed' }
    python -m pytest -q '.\phase166_r3c_stage2\test_stage2.py' '.\tests\test_phase165_r3_recursive_search.py' '.\phase166_r3_ordered_lookup\tests\test_phase166_r3_ordered_lookup.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C stage 2 focused tests failed' }
    Write-Host 'R3-C stage 2 targeted PASS; full pytest NOT run.'
} finally { Pop-Location }
