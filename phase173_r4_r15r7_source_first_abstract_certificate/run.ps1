param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R7 Git fetch failed' }

    python -m phase173_r4_r15r7_source_first_abstract_certificate.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R7 source preflight failed' }

    python -m pytest -q phase173_r4_r15r7_source_first_abstract_certificate/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R7 static tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R7_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R7_PRODUCTION_EDIT=NONE'
    } else {
        python -m pytest -q `
            phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
            phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
            phase173_r4_r10_general_toda56_core/tests/test_core.py `
            phase173_r4_r11_zero_public_connection/tests/test_route.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R7 focused pytest failed' }
        Write-Output 'PHASE173_R4_R15R7_FOCUSED_PYTEST=PASS'

        python -m phase173_r4_r15r7_source_first_abstract_certificate.audit `
            --root "$Root" `
            --output (Join-Path $PSScriptRoot 'abstract_certificate_report.json')
        if ($LASTEXITCODE -ne 0) { throw 'R15R7 source-first abstract audit failed' }
        Write-Output 'PHASE173_R4_R15R7_PHASE_COMPLETED=False'
    }
} finally {
    Pop-Location
}
