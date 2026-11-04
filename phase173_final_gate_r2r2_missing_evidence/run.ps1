param([switch]$DryRun)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'

$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root --no-pager rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
    throw 'Git repository root not found'
}
if (-not [string]::Equals(
    [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/'),
    [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/'),
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw 'Extract R2R2 ZIP at EHP repository root'
}

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_R2R2_SCOPE=MISSING_PRIOR_EVIDENCE_ACKNOWLEDGEMENT_ONLY'
    Write-Output 'PHASE173_FINAL_R2R2_FULL_PYTEST=False'
    Write-Output 'PHASE173_FINAL_R2R2_PRODUCTION_WRITES=NONE'
    Write-Output 'PHASE173_FINAL_R2R2_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Failed to read Git index tree' }

    Write-Output '=== R2R2 REVIEWED PATCH CONTRACT TESTS ==='
    & python -B -m pytest -q --tb=short -p no:cacheprovider `
        phase173_final_gate_r2r2_missing_evidence/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R2R2 patch contract tests failed' }

    if ($DryRun) {
        & python -B -m phase173_final_gate_r2r2_missing_evidence.patch `
            --repo $Root --package $Package
        if ($LASTEXITCODE -ne 0) { throw 'R2R2 reviewed source guard failed' }
        Write-Output 'PHASE173_FINAL_R2R2_DRY_RUN=PASS'
        Write-Output 'PHASE173_FINAL_R2R2_PRODUCTION_WRITES=NONE'
    } else {
        & python -B -m phase173_final_gate_r2r2_missing_evidence.patch `
            --repo $Root --package $Package --apply
        if ($LASTEXITCODE -ne 0) { throw 'R2R2 install failed' }
        Write-Output '=== R2R2 UPDATED R2 GATE FOCUSED TESTS ==='
        & python -B -m pytest -q --tb=short -p no:cacheprovider `
            phase173_final_gate_r2_recovery/tests/test_gate_contract.py `
            phase173_final_gate_r2r2_missing_evidence/tests/test_patch_contract.py
        if ($LASTEXITCODE -ne 0) {
            & python -B -m phase173_final_gate_r2r2_missing_evidence.patch `
                --repo $Root --package $Package --rollback
            throw 'R2R2 focused pytest failed; reviewed original R2 files restored'
        }
        Write-Output 'PHASE173_FINAL_R2R2_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE173_FINAL_R2R2_APPLY=PASS'
    }

    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $BeforeIndex -ne $AfterIndex) {
        throw 'R2R2 modified Git index'
    }
    Write-Output 'PHASE173_FINAL_R2R2_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
    & git --no-pager diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed' }
}
finally {
    Pop-Location
}
