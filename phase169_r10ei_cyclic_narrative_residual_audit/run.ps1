$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path (Join-Path $Package 'output') ('run_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'))
Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R10EI requires local develop branch'
    }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EI could not read HEAD' }
    Write-Host "R10EI_BRANCH=$Branch"
    Write-Host "R10EI_HEAD=$Head"
    & git merge-base --is-ancestor '1a132f382b4fe93b1ab3cb30f5d9178684e9c65a' HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'R10EI requires reviewed Phase 169 R10EG commit ancestry'
    }
    $Known = [ordered]@{
        'phase168_r3_5_model_renderer.py' = '2685ef3ef6bf7bc1673dededef1e3487d9941362'
        'phase168_r3_27_typed_statement_projection.py' = '57d0fb8cb713e91b0743f746bc8d59cea648868e'
        'phase169_r10a_verified_stable_chain_projection/projection.py' = 'c387b6a46d71561f8ecc2f2dc1d78158145dd883'
        'phase169_r10ec_direct_sum_narrative_projection/projection.py' = 'ace11ebd4841ac81592ef4f948507e63bc9f6038'
        'phase169_r10e1_general_group_transport/transport.py' = '3865d1e57923a0d45f0240cc357110e51b20a3e1'
        'phase169_r10b_registered_stable_family_binding/family_registry.py' = '4e461795954cc3e7a34fe9e3b47f77d00e5faeda'
        'phase169_r10d2_general_family_definition/family_citation.py' = '91587dcd19c96a7bd069a2e009b70c2e5aa9b378'
    }
    foreach ($Relative in $Known.Keys) {
        $Blob = (& git rev-parse "HEAD:$Relative").Trim()
        if ($LASTEXITCODE -ne 0 -or $Blob -ne $Known[$Relative]) {
            throw "R10EI reviewed Git blob mismatch: $Relative"
        }
        & git diff --quiet HEAD -- $Relative
        if ($LASTEXITCODE -ne 0) {
            throw "R10EI working file differs from reviewed commit: $Relative"
        }
    }
    Write-Host 'R10EI_REVIEWED_DEPENDENCIES=PASS'
    Write-Host 'R10EI_MODE=AUDIT_ONLY'
    $Before = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EI status before failed' }
    Write-Host "R10EI_TRACKED_BEFORE_COUNT=$($Before.Count)"
    $Tests = @('.\phase169_r10ei_cyclic_narrative_residual_audit\tests\test_r10ei_diagnostics.py')
    & python -B -m pytest -q -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R10EI focused pytest failed' }
    & python -B -m phase169_r10ei_cyclic_narrative_residual_audit.audit $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EI real-group residual audit requires review' }
    $After = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EI status after failed' }
    if (($Before -join "`n") -ne ($After -join "`n")) {
        Write-Host ('R10EI_TRACKED_BEFORE=' + ($Before -join ' || '))
        Write-Host ('R10EI_TRACKED_AFTER=' + ($After -join ' || '))
        throw 'R10EI tracked files changed unexpectedly; no restore was attempted'
    }
    Write-Host 'R10EI_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Host 'R10EI_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10EI_FULL_PYTEST_RUN=False'
    Write-Host 'R10EI_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host "R10EI_OUTPUT=$Output"
}
finally {
    Pop-Location
}
