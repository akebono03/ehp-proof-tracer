param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 GitHub fetch failed' }

    python -m phase173_r4_r15r14_common_partial_presentation.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r14_common_partial_presentation/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 pure contract tests failed' }

    if ($DryRun) {
        Write-Output 'R15R14_DRY_RUN=PASS'
        Write-Output 'R15R14_PRODUCTION_CODE_EDIT=NONE'
        Write-Output 'R15R14_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r14_common_partial_presentation.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 installation failed' }

    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r14_common_partial_presentation/tests/test_contract.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_contract.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R14 focused pytest failed' }
        Write-Output 'R15R14_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R14_FULL_PYTEST_RUN=False'
        Write-Output 'R15R14_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r14_common_partial_presentation.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R14 rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
