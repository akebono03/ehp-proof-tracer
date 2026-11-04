param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    python -m phase173_r4_r15r15_abstract_result_banner.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R15 source guard failed' }
    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r15_abstract_result_banner/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R15 contract tests failed' }
    if ($DryRun) {
        Write-Output 'R15R15_DRY_RUN=PASS'
        Write-Output 'R15R15_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r15_abstract_result_banner.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R15 installation failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r15_abstract_result_banner/tests/test_contract.py `
            phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
            tests/test_phase117_web_app.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R15 focused pytest failed' }
        Write-Output 'R15R15_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R15_FULL_PYTEST_RUN=False'
        Write-Output 'R15R15_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r15_abstract_result_banner.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R15 rollback failed; inspect backups' }
        throw
    }
} finally {
    Pop-Location
}
