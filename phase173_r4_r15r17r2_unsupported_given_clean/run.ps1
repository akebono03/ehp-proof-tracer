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
    $GitRoot = & git --no-pager rev-parse --show-toplevel
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
        throw 'Cannot determine the Git repository root'
    }
    # Git on Windows typically prints C:/... while Resolve-Path prints C:\...
    # Compare canonical filesystem paths, not their original text spellings.
    $ActualRoot = [System.IO.Path]::GetFullPath($GitRoot.Trim())
    $ExpectedRoot = [System.IO.Path]::GetFullPath($Root)
    if (-not [string]::Equals(
        $ActualRoot,
        $ExpectedRoot,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw 'Extract R15R17-R2 ZIP at the repository root'
    }
    Write-Output 'R15R17R2_REPOSITORY_ROOT=PASS'
    Write-Output 'R15R17R2_SCOPE=UNRENDERABLE_PARTIAL_STEP_ONLY'
    Write-Output 'R15R17R2_FULL_PYTEST=False'
    Write-Output 'R15R17R2_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
    if ($Restore) {
        & python -m phase173_r4_r15r17r2_unsupported_given_clean.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R2 restore failed' }
        return
    }
    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub develop fetch failed' }
    Write-Output '=== R15R17-R2 PATCH CONTRACT ==='
    & python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r17r2_unsupported_given_clean/tests/test_patch_contract.py `
      phase173_r4_r15r17r2_unsupported_given_clean/tests/test_path_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R2 patch contract failed' }
    if ($DryRun) {
        & python -m phase173_r4_r15r17r2_unsupported_given_clean.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R2 DryRun failed' }
        Write-Output 'R15R17R2_DRY_RUN=PASS'
        return
    }
    & python -m phase173_r4_r15r17r2_unsupported_given_clean.install
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R2 install failed' }
    try {
        Write-Output '=== R15R17-R2 FOCUSED PYTEST ==='
        & python -m pytest -q -p no:cacheprovider `
          phase173_r4_r15r17r2_unsupported_given_clean/tests/test_public_narrative.py `
          phase173_r4_r15r17_unified_model/tests/test_unified_web.py `
          phase173_r4_r15r12_reference_correction/tests/test_integration.py::test_other_completed_groups_not_promoted_or_downgraded
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R2 focused pytest failed' }
        Write-Output 'R15R17R2_FOCUSED_PYTEST=PASS'
    }
    catch {
        Write-Output 'R15R17R2_FOCUSED_PYTEST=FAIL; restoring only the R2 renderer change'
        & python -m phase173_r4_r15r17r2_unsupported_given_clean.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'Automatic restore also failed; inspect state and backup' }
        throw
    }
    Write-Output 'R15R17R2_APPLY=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
}
finally {
    Pop-Location
}
