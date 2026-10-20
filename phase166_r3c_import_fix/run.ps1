$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Project
try {
    $env:PYTHONPATH = $Project
    if (-not (Test-Path '.\phase166_r3b_publication_order_binding\phase166_r3b_publication_order_binding.py')) {
        throw 'R3-B implementation module missing. No changes made.'
    }
    python -c "from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import connect_phase163_publication_order; from phase165_r3_recursive_search import reconstruct_registered_goal; print('R3-C import OK')"
    if ($LASTEXITCODE -ne 0) { throw 'R3-C import check failed' }
    python -m pytest -q '.\phase166_r3c_ordered_search\tests\test_phase166_r3c_ordered_search.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3-C targeted tests failed' }
    Write-Host 'Phase 166 R3-C targeted PASS; full pytest NOT run.'
} finally { Pop-Location }
