$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python '.\phase166_r3c_reimplementation\install.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C install failed' }
    python -m pytest -q '.\phase166_r3c_reimplementation\tests\test_r3c_reimplementation.py' '.\tests\test_phase166_r3b_publication_order_binding.py' '.\tests\test_phase165_r3_recursive_search.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C targeted pytest failed' }
    Write-Host 'Phase 166 R3-C repair targeted PASS; full pytest NOT run.'
    Write-Host 'Next: Web n=2,k=1 complete-proof check is required.'
} finally { Pop-Location }
