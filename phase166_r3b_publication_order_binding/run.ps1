$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Project
try {
    $env:PYTHONPATH = $Project

    Copy-Item -LiteralPath '.\phase166_r3b_publication_order_binding\phase166_r3b_publication_order_binding.py' -Destination '.\phase166_r3b_publication_order_binding.py' -Force
    Copy-Item -LiteralPath '.\phase166_r3b_publication_order_binding\test_phase166_r3b_publication_order_binding.py' -Destination '.\tests\test_phase166_r3b_publication_order_binding.py' -Force

    python -m pytest -q `
        '.\tests\test_phase166_r3b_publication_order_binding.py' `
        '.\tests\test_phase165_r5_manifest_bridge.py' `
        '.\tests\test_phase163_r2_unified_registry.py'
    if ($LASTEXITCODE -ne 0) { throw 'Phase 166 R3-B targeted tests failed' }

    python '.\phase166_r3b_publication_order_binding\audit.py' | Tee-Object -FilePath '.\phase166_r3b_publication_order_binding\audit_result.json'
    if ($LASTEXITCODE -ne 0) { throw 'Phase 166 R3-B audit failed' }

    Write-Host 'Phase 166 R3-B targeted PASS; full pytest NOT run.'
} finally {
    Pop-Location
}
