param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Git fetch failed' }
    python -m phase173_r4_r15r2_generator_obligation_audit.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 Preflight failed' }
    python -m pytest -q `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_static.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_head_lineage.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R2_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R2_PRODUCTION_EDIT=NONE'
        exit 0
    }
    python -m pytest -q `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 focused tests failed' }
    Write-Output 'PHASE173_R4_R15R2_FOCUSED_PYTEST=PASS'
    python -m phase173_r4_r15r2_generator_obligation_audit.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'factor_obligation_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 factor audit failed' }
    Write-Output 'PHASE173_R4_R15R2_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
