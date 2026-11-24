param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsForAudit = @()
    if ($DryRun) { $argsForAudit += '--dry-run' }
    & python -B -m phase176_r3r40_toda55_connection_audit.audit @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R3R40 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r40_toda55_connection_audit\tests\test_connection.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R40 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R40 git diff check failed' }
        Write-Host 'PHASE176_R3R40_GATE=PASS_R3R40_TODA55_CONNECTION_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R40_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
