param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    & python -B -m phase173_r4_r13r1_head_lineage_fix.repair --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13R1 reviewed preflight failed' }
    Write-Output 'PHASE173_R4_R13R1_FOCUSED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        'phase173_r4_r13r1_head_lineage_fix/tests/test_repair.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13R1 focused tests failed' }
    Write-Output 'PHASE173_R4_R13R1_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R13R1_RESULT=PASS_DRY_RUN'
        exit 0
    }
    & python -B -m phase173_r4_r13r1_head_lineage_fix.repair --root $Root
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13R1 source guard correction failed' }
    & powershell -NoProfile -ExecutionPolicy Bypass `
        -File '.\phase173_r4_r13_narrative_audit\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13 corrected DryRun failed' }
    & powershell -NoProfile -ExecutionPolicy Bypass `
        -File '.\phase173_r4_r13_narrative_audit\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13 corrected read-only audit failed' }
    Write-Output 'PHASE173_R4_R13R1_RESULT=PASS'
} finally {
    Pop-Location
}
