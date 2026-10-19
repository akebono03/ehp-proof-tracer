$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q phase165_r6_phase163_prop51/test_phase163_prop51_adopted.py
    if ($LASTEXITCODE -ne 0) { throw 'Phase163 adopted input targeted tests failed' }
    Write-Host 'Phase163 Proposition 5.1 adopted typed tests PASS; full pytest NOT run'
} finally { Pop-Location }
