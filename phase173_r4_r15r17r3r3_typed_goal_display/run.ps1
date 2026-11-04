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
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
        throw 'Cannot determine Git repository root'
    }
    $ActualRoot = [System.IO.Path]::GetFullPath($GitRoot.Trim())
    $ExpectedRoot = [System.IO.Path]::GetFullPath($Root)
    if (-not [string]::Equals(
        $ActualRoot, $ExpectedRoot, [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw 'Extract R15R17-R3R3 ZIP at the repository root'
    }
    Write-Output 'R15R17R3R3_REPOSITORY_ROOT=PASS'
    Write-Output 'R15R17R3R3_SCOPE=TYPED_OPEN_GOAL_DISPLAY_ONLY'
    Write-Output 'R15R17R3R3_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'R15R17R3R3_FULL_PYTEST=False'

    if ($Restore) {
        & python -m phase173_r4_r15r17r3r3_typed_goal_display.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R3 restore failed' }
        return
    }

    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub develop fetch failed' }

    Write-Output '=== R15R17-R3R3 PATCH CONTRACT ==='
    & python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r17r3r3_typed_goal_display/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R3 contract tests failed' }

    if ($DryRun) {
        & python -m phase173_r4_r15r17r3r3_typed_goal_display.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R3 DryRun failed' }
        Write-Output 'R15R17R3R3_DRY_RUN=PASS'
        return
    }

    & python -m phase173_r4_r15r17r3r3_typed_goal_display.install
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R3 installation failed' }
    try {
        Write-Output '=== R15R17-R3R3 FOCUSED PYTEST ==='
        & python -m pytest -q -p no:cacheprovider `
          phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py `
          phase173_r4_r15r17r2_unsupported_given_clean/tests/test_public_narrative.py `
          phase173_r4_r15r17_unified_model/tests/test_unified_web.py `
          phase173_r4_r15r12_reference_correction/tests/test_integration.py::test_other_completed_groups_not_promoted_or_downgraded
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R3 focused pytest failed' }
        Write-Output 'R15R17R3R3_FOCUSED_PYTEST=PASS'
    }
    catch {
        Write-Output 'R15R17R3R3_FOCUSED_PYTEST=FAIL; restoring only R3R3 renderer change'
        & python -m phase173_r4_r15r17r3r3_typed_goal_display.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'Automatic R3R3 restore failed; inspect installed_state.json and backup' }
        throw
    }
    Write-Output 'R15R17R3R3_APPLY=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
}
finally {
    Pop-Location
}
