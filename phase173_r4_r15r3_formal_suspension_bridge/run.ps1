param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 Git fetch failed' }
    python -m phase173_r4_r15r3_formal_suspension_bridge.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 Preflight failed' }
    python -m pytest -q `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_static.py `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R3_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R3_PRODUCTION_EDIT=NONE'
        exit 0
    }
    python -m pytest -q `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R3_FOCUSED_PYTEST=PASS'
    python -m phase173_r4_r15r3_formal_suspension_bridge.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'formal_image_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 audit failed' }
    Write-Output 'PHASE173_R4_R15R3_PUBLIC_COMPLETION=False'
    Write-Output 'PHASE173_R4_R15R3_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
