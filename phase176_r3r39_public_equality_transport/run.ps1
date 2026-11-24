param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsForPatch = @()
    if ($DryRun) { $argsForPatch += '--dry-run' }
    & python -B -m phase176_r3r39_public_equality_transport.apply @argsForPatch
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 patch failed' }
    $argsForAudit = @()
    if ($DryRun) { $argsForAudit += '--dry-run' }
    & python -B -m phase176_r3r39_public_equality_transport.audit @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py `
            .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
            .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
            .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R39 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R39 git diff check failed' }
        Write-Host 'PHASE176_R3R39_GATE=PASS_R3R39_PUBLIC_SOURCED_DFS_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R39_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
