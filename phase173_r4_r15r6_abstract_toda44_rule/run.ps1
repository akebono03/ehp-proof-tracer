param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 Git fetch failed' }

    python -m phase173_r4_r15r6_abstract_toda44_rule.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 source preflight failed' }

    python -m pytest -q `
        phase173_r4_r15r6_abstract_toda44_rule/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 static tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R6_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R6_PRODUCTION_EDIT=NONE'
        exit 0
    }

    python -m pytest -q `
        phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
        phase173_r4_r15r5_family_source_frontier/tests/test_integration.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R6_FOCUSED_PYTEST=PASS'

    python -m phase173_r4_r15r6_abstract_toda44_rule.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'abstract_toda44_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 abstract root audit failed' }
    Write-Output 'PHASE173_R4_R15R6_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
