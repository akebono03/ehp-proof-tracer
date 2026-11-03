param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    & python -B -m phase173_r4_r13_narrative_audit.audit --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13 source guard or dry-run failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R13_RESULT=PASS_DRY_RUN'
        exit 0
    }
    Write-Output 'PHASE173_R4_R13_FOCUSED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        'phase173_r4_r13_narrative_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13 focused narrative tests failed' }
    Write-Output 'PHASE173_R4_R13_FOCUSED_PYTEST=PASS'
    & python -B -m phase173_r4_r13_narrative_audit.audit --root $Root
    if ($LASTEXITCODE -ne 0) { throw 'R4-R13 five-group source and Web audit failed' }
    Write-Output 'PHASE173_R4_R13_AUDIT_ONLY=PASS'
} finally {
    Pop-Location
}
