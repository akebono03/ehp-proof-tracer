$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path (Join-Path $Package 'output') ('run_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'))
Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') { throw 'R10EH requires local develop' }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EH failed to read HEAD' }
    Write-Host "R10EH_BRANCH=$Branch"
    Write-Host "R10EH_HEAD=$Head"
    & git merge-base --is-ancestor '1a132f382b4fe93b1ab3cb30f5d9178684e9c65a' HEAD
    if ($LASTEXITCODE -ne 0) { throw 'R10EH-R1 requires reviewed R10EG ancestry' }
    $Known = [ordered]@{
        'phase169_r10a_verified_stable_chain_projection/projection.py' = 'c387b6a46d71561f8ecc2f2dc1d78158145dd883'
        'phase169_r10ec_direct_sum_narrative_projection/projection.py' = 'ace11ebd4841ac81592ef4f948507e63bc9f6038'
        'phase169_r10b_registered_stable_family_binding/family_registry.py' = '4e461795954cc3e7a34fe9e3b47f77d00e5faeda'
        'phase169_r10d2_general_family_definition/family_citation.py' = '91587dcd19c96a7bd069a2e009b70c2e5aa9b378'
        'phase168_r3_5_model_renderer.py' = '2685ef3ef6bf7bc1673dededef1e3487d9941362'
        'phase169_r10e1_general_group_transport/transport.py' = '3865d1e57923a0d45f0240cc357110e51b20a3e1'
    }
    foreach ($relative in $Known.Keys) {
        $blob = (& git rev-parse "HEAD:$relative").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $Known[$relative]) {
            throw "R10EH reviewed Git blob mismatch: $relative"
        }
    }
    $Target = Join-Path $Repo 'phase169_r10e1_general_group_transport\transport.py'
    $Text = [System.IO.File]::ReadAllText($Target)
    $LocalTransportBlob = (& git hash-object -- $Target).Trim()
    if ($LASTEXITCODE -ne 0 -or $LocalTransportBlob -ne $Known['phase169_r10e1_general_group_transport/transport.py']) {
        throw 'R10EH-R1 working transport.py differs from reviewed R10EG blob'
    }
    if (-not $Text.Contains('# R10EG: established eta-specific 1-stem derivations')) {
        throw 'R10EH requires successful R10EG locally applied or committed'
    }
    Write-Host 'R10EH_REVIEWED_GITHUB_DEPENDENCIES=PASS'
    Write-Host 'R10EH_R10EG_PRECONDITION=PASS'
    Write-Host 'R10EH_SCOPE=AUDIT_ONLY'
    $Before = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EH could not read before Git status' }
    Write-Host "R10EH_EXISTING_TRACKED_CHANGES=$($Before.Count)"
    # Only a new run-stamped, untracked output directory is written.
    $Tests = @('.\phase169_r10eh_stem6_10_11_14_audit\tests\test_r10eh_policy.py')
    & python -B -m pytest -q -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R10EH focused policy tests failed' }
    & python -B -m phase169_r10eh_stem6_10_11_14_audit.audit $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EH observed unexpected proof status or trust failure' }
    $After = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EH could not read after Git status' }
    if (($Before -join "`n") -ne ($After -join "`n")) {
        Write-Host ('R10EH_TRACKED_BEFORE=' + ($Before -join ' || '))
        Write-Host ('R10EH_TRACKED_AFTER=' + ($After -join ' || '))
        throw 'R10EH tracked file status changed'
    }
    Write-Host 'R10EH_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Host 'R10EH_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10EH_FULL_PYTEST_RUN=False'
    Write-Host 'R10EH_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host "R10EH_OUTPUT=$Output"
}
finally {
    Pop-Location
}
