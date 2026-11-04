param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 git fetch failed' }

    python -m phase173_r4_r15r16r3_staged_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r16r3_staged_guard_fix/tests/test_preview.py `
        phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 preview tests failed' }

    if ($DryRun) {
        Write-Output 'R15R16R3_DRY_RUN=PASS'
        Write-Output 'R15R16R3_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r16r3_staged_guard_fix.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 install failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r16r3_staged_guard_fix/tests/test_preview.py `
            phase173_r4_r15r16r3_staged_guard_fix/tests/test_adapter_unit.py `
            phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_contract.py `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py `
            phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 focused regression failed' }
        Write-Output 'R15R16R3_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R16R3_FULL_PYTEST_RUN=False'
        Write-Output 'R15R16R3_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r16r3_staged_guard_fix.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
