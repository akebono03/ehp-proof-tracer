param(
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'
$env:PYTHONDONTWRITEBYTECODE = '1'

$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Git root is not accessible' }
$Actual = [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/')
$Expected = [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/')
if (-not [string]::Equals($Actual, $Expected, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Extract this ZIP in the repository root'
}

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_R1_SCOPE=PHASE167_REFERENCE_TEST_CONTRACT_ONLY'
    Write-Output 'PHASE173_FINAL_R1_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'PHASE173_FINAL_R1_FULL_PYTEST=False'
    Write-Output 'PHASE173_FINAL_R1_PRIOR_FAILED_GATE_REPORT=PRESERVED'
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git index' }
    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch origin/develop' }

    Write-Output '=== PHASE 173 FINAL R1 OFFLINE PATCH TESTS ==='
    & python -B -m pytest -q --tb=short -p no:cacheprovider `
        phase173_final_gate_r1_phase167_reference_contract/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final R1 patch contract failed' }

    if ($DryRun) {
        & python -B -m phase173_final_gate_r1_phase167_reference_contract.patch `
            dry-run --repo $Root --package $Package
        if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final R1 DryRun failed' }
        Write-Output 'PHASE173_FINAL_R1_FULL_CHANGED_UNITS=phase173_final_gate_r1_phase167_reference_contract/FULL_CHANGED_UNITS.md'
        Write-Output 'PHASE173_FINAL_R1_DRY_RUN=PASS'
    }
    else {
        $Applied = $false
        try {
            & python -B -m phase173_final_gate_r1_phase167_reference_contract.patch `
                apply --repo $Root --package $Package
            if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final R1 installation failed' }
            $Applied = $true

            Write-Output '=== PHASE 173 FINAL R1 FOCUSED TESTS (NOT THE FULL SUITE) ==='
            & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider `
                tests/test_phase167_r2_range_dedup.py `
                tests/test_phase167_r2_shared_reference.py `
                tests/test_phase167_r2_unified_reference.py
            if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final R1 focused pytest failed' }
            Write-Output 'PHASE173_FINAL_R1_FOCUSED_PYTEST=PASS'
            Write-Output 'PHASE173_FINAL_R1_APPLY=PASS'
        }
        catch {
            if ($Applied) {
                & python -B -m phase173_final_gate_r1_phase167_reference_contract.patch `
                    rollback --repo $Root --package $Package
                if ($LASTEXITCODE -ne 0) {
                    Write-Output 'PHASE173_FINAL_R1_ROLLBACK_REQUIRES_REVIEW=True'
                }
            }
            throw
        }
    }
    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $BeforeIndex -ne $AfterIndex) {
        throw 'Phase 173 final R1 changed the Git index'
    }
    Write-Output 'PHASE173_FINAL_R1_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
    & git --no-pager diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed' }
}
finally {
    Pop-Location
}
