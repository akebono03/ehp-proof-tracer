param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 Git fetch failed' }
    python -m phase173_r4_r15r4_cited_composition_image.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 Preflight failed' }
    python -m pytest -q `
        phase173_r4_r15r4_cited_composition_image/tests/test_static.py `
        phase173_r4_r15r4_cited_composition_image/tests/test_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 isolated tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R4_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R4_PRODUCTION_EDIT=NONE'
        exit 0
    }
    python -m pytest -q `
        phase173_r4_r15r4_cited_composition_image/tests/test_integration.py `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R4_FOCUSED_PYTEST=PASS'
    python -m phase173_r4_r15r4_cited_composition_image.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'source_cited_image_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 cited-image audit failed' }
    Write-Output 'PHASE173_R4_R15R4_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
