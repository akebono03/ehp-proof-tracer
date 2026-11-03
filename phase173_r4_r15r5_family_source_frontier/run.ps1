param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 Git fetch failed' }

    python -m phase173_r4_r15r5_family_source_frontier.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 source preflight failed' }

    python -m pytest -q `
        phase173_r4_r15r5_family_source_frontier/tests/test_static.py `
        phase173_r4_r15r5_family_source_frontier/tests/test_scan.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 standalone tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R5_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R5_PRODUCTION_EDIT=NONE'
        exit 0
    }

    python -m pytest -q `
        phase173_r4_r15r5_family_source_frontier/tests/test_integration.py `
        phase173_r4_r15r4_cited_composition_image/tests/test_integration.py `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R5_FOCUSED_PYTEST=PASS'

    python -m phase173_r4_r15r5_family_source_frontier.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'family_source_frontier_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 source frontier audit failed' }
    Write-Output 'PHASE173_R4_R15R5_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
