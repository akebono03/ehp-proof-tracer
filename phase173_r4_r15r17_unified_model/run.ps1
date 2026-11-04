param(
    [switch]$DryRun,
    [switch]$Restore
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $ActualRoot = (& git --no-pager rev-parse --show-toplevel).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Not a Git repository' }
    if ([IO.Path]::GetFullPath($ActualRoot).TrimEnd('\', '/') -ne [IO.Path]::GetFullPath($Root).TrimEnd('\', '/')) {
        throw 'R15R17 must be extracted at the repository root'
    }

    Write-Output 'R15R17_SCOPE=ONE_MODEL_ONE_RENDERER'
    Write-Output 'R15R17_FULL_PYTEST=False'
    Write-Output 'R15R17_GIT_PAGER_DISABLED=True'
    Write-Output 'R15R17_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'

    if ($Restore) {
        & python -m phase173_r4_r15r17_unified_model.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R17 restore failed' }
        return
    }

    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R17 remote fetch failed' }

    Write-Output '=== R15R17 PATCH CONTRACT TESTS ==='
    & python -m pytest -q phase173_r4_r15r17_unified_model/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R17 patch contract test failed' }

    if ($DryRun) {
        & python -m phase173_r4_r15r17_unified_model.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R17 DryRun source review failed' }
        Write-Output 'R15R17_DRY_RUN=PASS'
        return
    }

    & python -m phase173_r4_r15r17_unified_model.install
    if ($LASTEXITCODE -ne 0) { throw 'R15R17 source install failed' }

    try {
        Write-Output '=== R15R17 FOCUSED PYTEST ==='
        & python -m pytest -q `
          phase173_r4_r15r17_unified_model/tests/test_unified_web.py `
          phase173_r4_r15r12_reference_correction/tests/test_integration.py::test_other_completed_groups_not_promoted_or_downgraded `
          phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R17 focused pytest failed' }
        Write-Output 'R15R17_FOCUSED_PYTEST=PASS'
    }
    catch {
        Write-Output 'R15R17_FOCUSED_PYTEST=FAIL; guarded restore starts'
        & python -m phase173_r4_r15r17_unified_model.install --restore
        if ($LASTEXITCODE -ne 0) {
            throw 'R15R17 focused tests failed and automatic restore also failed: inspect installed_state.json and backups'
        }
        throw
    }
    Write-Output 'R15R17_APPLY=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'R15R17 git status failed' }
}
finally {
    Pop-Location
}
