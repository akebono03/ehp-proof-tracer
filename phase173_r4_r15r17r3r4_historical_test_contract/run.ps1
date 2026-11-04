param(
    [switch]$DryRun,
    [switch]$Restore
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'
$env:PYTHONDONTWRITEBYTECODE = '1'

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $GitRoot = & git --no-pager rev-parse --show-toplevel
    if ($LASTEXITCODE -ne 0) { throw 'Git repository root not found' }
    $Expected = [System.IO.Path]::GetFullPath($Root)
    $Actual = [System.IO.Path]::GetFullPath($GitRoot.Trim())
    if (-not [string]::Equals($Expected, $Actual, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw 'Extract R15R17-R3R4 ZIP at the repository root'
    }
    Write-Output 'R15R17R3R4_REPOSITORY_ROOT=PASS'
    Write-Output 'R15R17R3R4_SCOPE=HISTORICAL_TEST_CONTRACT_ONLY'
    Write-Output 'R15R17R3R4_FULL_PYTEST=False'
    Write-Output 'R15R17R3R4_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'

    if ($Restore) {
        & python -m phase173_r4_r15r17r3r4_historical_test_contract.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R4 restore failed' }
        return
    }

    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch GitHub develop' }
    Write-Output '=== R15R17-R3R4 PATCH CONTRACT ==='
    & python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r17r3r4_historical_test_contract/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R4 patch contract failed' }

    if ($DryRun) {
        & python -m phase173_r4_r15r17r3r4_historical_test_contract.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R4 DryRun failed' }
        Write-Output 'R15R17R3R4_DRY_RUN=PASS'
        return
    }

    & python -m phase173_r4_r15r17r3r4_historical_test_contract.install
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R4 installation failed' }
    try {
        Write-Output '=== R15R17-R3R4 FOCUSED PYTEST (historical regression) ==='
        & python -m pytest -q -p no:cacheprovider `
          phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
          phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
          phase173_r4_r15r12_reference_correction/tests/test_integration.py `
          phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
          phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
          phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py `
          phase173_r4_r15r15r2_head_guard_fix/tests/test_integration.py `
          phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py `
          phase173_r4_r15r16r2_shared_tree_narrative/tests/test_integration.py `
          phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py `
          phase173_r4_r15r17r3r4_historical_test_contract/tests/test_unified_public_contract.py `
          phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py `
          phase173_r4_r15r17_unified_model/tests/test_unified_web.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R4 focused pytest failed' }
        Write-Output 'R15R17R3R4_FOCUSED_PYTEST=PASS'
    }
    catch {
        Write-Output 'R15R17R3R4_FOCUSED_PYTEST=FAIL; restoring only R3R4 test files'
        & python -m phase173_r4_r15r17r3r4_historical_test_contract.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'Automatic test-only restore failed; inspect backups' }
        throw
    }
    Write-Output 'R15R17R3R4_APPLY=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
}
finally {
    Pop-Location
}
