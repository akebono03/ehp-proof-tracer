param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $mode = @()
    if ($DryRun) { $mode += '--dry-run' }
    & python -B -m phase176_r3r41_public_quadruple_connection.apply @mode
    if ($LASTEXITCODE -ne 0) { throw 'R3R41 patch failed' }
    & python -B -m phase176_r3r41_public_quadruple_connection.audit @mode
    if ($LASTEXITCODE -ne 0) { throw 'R3R41 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r41_public_quadruple_connection\tests\test_apply.py `
            .\phase176_r3r41_public_quadruple_connection\tests\test_public_connection.py `
            .\phase176_r3r40r1_eta_notation_bridge\tests\test_notation.py `
            .\phase176_r3r40_toda55_connection_audit\tests\test_connection.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R41 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R41 git diff check failed' }
        Write-Host 'PHASE176_R3R41_GATE=PASS_R3R41_PUBLIC_QUADRUPLE_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R41R1_GATE=PASS_R3R41R1_SCOPED_PATCH_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R41_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally { Pop-Location }
