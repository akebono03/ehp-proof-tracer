param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    python -m phase173_r4_r15r13_unified_presentation.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Source guard failed' }
    python -m pytest -q -p no:cacheprovider phase173_r4_r15r13_unified_presentation/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'Pure contract tests failed' }

    if ($DryRun) {
        Write-Output 'R15R13_UNIFIED_DRY_RUN=PASS'
        Write-Output 'R15R13_UNIFIED_PHASE_COMPLETED=False'
        exit 0
    }
    python -m phase173_r4_r15r13_unified_presentation.install --install
    if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r13_unified_presentation/tests/test_contract.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
            phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py `
            phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py
        if ($LASTEXITCODE -ne 0) { throw 'Focused regression tests failed' }
        Write-Output 'R15R13_UNIFIED_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R13_UNIFIED_FULL_PYTEST_RUN=False'
        Write-Output 'R15R13_UNIFIED_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r13_unified_presentation.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'Rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
