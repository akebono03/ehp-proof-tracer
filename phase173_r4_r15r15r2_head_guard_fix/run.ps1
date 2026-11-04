param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    python -m phase173_r4_r15r15r2_head_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 source guard failed' }
    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r15r2_head_guard_fix/tests/test_contract.py `
        phase173_r4_r15r15r2_head_guard_fix/tests/test_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 contract tests failed' }
    if ($DryRun) {
        Write-Output 'R15R15R2_DRY_RUN=PASS'
        Write-Output 'R15R15R2_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r15r2_head_guard_fix.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 install failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r15r2_head_guard_fix/tests/test_contract.py `
            phase173_r4_r15r15r2_head_guard_fix/tests/test_guard.py `
            phase173_r4_r15r15r2_head_guard_fix/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
            tests/test_phase117_web_app.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 focused pytest failed' }
        Write-Output 'R15R15R2_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R15R2_FULL_PYTEST_RUN=False'
        Write-Output 'R15R15R2_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r15r2_head_guard_fix.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
