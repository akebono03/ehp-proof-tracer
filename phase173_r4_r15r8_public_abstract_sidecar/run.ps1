param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R8 git fetch failed' }

    python -m phase173_r4_r15r8_public_abstract_sidecar.install --root "$Root" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R8 source guard / preview failed' }

    python -m pytest -q phase173_r4_r15r8_public_abstract_sidecar/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R8 static tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R8_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R8_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r8_public_abstract_sidecar.install --root "$Root"
        if ($LASTEXITCODE -ne 0) { throw 'R15R8 installation failed' }
        try {
            python -m pytest -q `
                phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
                phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
                phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
                phase173_r4_r10_general_toda56_core/tests/test_core.py `
                phase173_r4_r11_zero_public_connection/tests/test_route.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R8 focused pytest failed' }
            Write-Output 'PHASE173_R4_R15R8_FOCUSED_PYTEST=PASS'

            python -m phase173_r4_r15r8_public_abstract_sidecar.audit --root "$Root" `
                --output (Join-Path $PSScriptRoot 'public_abstract_sidecar_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R8 audit failed' }
            Write-Output 'PHASE173_R4_R15R8_PHASE_COMPLETED=False'
        } catch {
            python -m phase173_r4_r15r8_public_abstract_sidecar.install --root "$Root" --restore
            throw
        }
    }
} finally {
    Pop-Location
}
