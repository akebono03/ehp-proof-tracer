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
    throw 'Extract Phase 173 R2R1 ZIP at repository root'
}

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_R2R1_SCOPE=PRIOR_EVIDENCE_PATH_AND_REVIEWED_FAST_FORWARD'
    Write-Output 'PHASE173_FINAL_R2R1_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
    Write-Output 'PHASE173_FINAL_R2R1_FULL_PYTEST=False'
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to record Git index tree' }

    Write-Output '=== R2R1 REVIEWED PATCH CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider `
        phase173_final_gate_r2r1_evidence_path_recovery/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R2R1 patch contract tests failed' }

    if ($DryRun) {
        & python -B -m phase173_final_gate_r2r1_evidence_path_recovery.patch `
            --repo $Root --package $Package
        if ($LASTEXITCODE -ne 0) { throw 'R2R1 DryRun source guard failed' }
        Write-Output 'PHASE173_FINAL_R2R1_DRY_RUN=PASS'
    }
    else {
        & python -B -m phase173_final_gate_r2r1_evidence_path_recovery.patch `
            --repo $Root --package $Package --apply
        if ($LASTEXITCODE -ne 0) { throw 'R2R1 install failed' }
        Write-Output '=== R2R1 CORRECTED R2 GATE FOCUSED TESTS ==='
        & python -B -m pytest -q -p no:cacheprovider `
            phase173_final_gate_r2_recovery/tests/test_gate_contract.py `
            phase173_final_gate_r2r1_evidence_path_recovery/tests/test_patch_contract.py
        if ($LASTEXITCODE -ne 0) {
            & python -B -m phase173_final_gate_r2r1_evidence_path_recovery.patch `
                --repo $Root --package $Package --rollback
            throw 'R2R1 focused pytest failed; original files restored'
        }
        Write-Output 'PHASE173_FINAL_R2R1_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE173_FINAL_R2R1_APPLY=PASS'
    }

    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $BeforeIndex -ne $AfterIndex) {
        throw 'R2R1 modified Git index'
    }
    Write-Output 'PHASE173_FINAL_R2R1_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git status' }
    & git --no-pager diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git diff' }
}
finally {
    Pop-Location
}
