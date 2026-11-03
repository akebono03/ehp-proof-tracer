param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R9 git fetch failed' }
    python -m phase173_r4_r15r9_shared_abstract_renderer.install --root "$RepoRoot" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R9 Source Guard failed' }
    python -m pytest -q -p no:cacheprovider phase173_r4_r15r9_shared_abstract_renderer/tests/test_static.py `
        phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R9 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R9_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R9_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r9_shared_abstract_renderer.install --root "$RepoRoot"
        if ($LASTEXITCODE -ne 0) { throw 'R15R9 installation failed' }
        try {
            python -m pytest -q -p no:cacheprovider `
                phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
                phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
                phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
                phase173_r4_r11_zero_public_connection/tests/test_route.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R9 focused pytest failed' }
            Write-Output 'PHASE173_R4_R15R9_FOCUSED_PYTEST=PASS'
            python -m phase173_r4_r15r9_shared_abstract_renderer.audit --root "$RepoRoot" `
                --output (Join-Path $PSScriptRoot 'shared_abstract_web_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R9 Web audit failed' }
            Write-Output 'PHASE173_R4_R15R9_PHASE_COMPLETED=False'
        } catch {
            python -m phase173_r4_r15r9_shared_abstract_renderer.install --root "$RepoRoot" --restore
            throw
        }
    }
} finally {
    Pop-Location
}
