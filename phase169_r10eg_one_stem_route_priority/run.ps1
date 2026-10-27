$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Relative = 'phase169_r10e1_general_group_transport/transport.py'
$Target = Join-Path $Repo 'phase169_r10e1_general_group_transport\transport.py'
$ExpectedBlob = 'd60770fff1b6e14791db6b952733f4062a64c8eb'
$Original = $null
$AttemptedPatch = $false
$Success = $false
$RunName = 'run_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff')
$Output = Join-Path (Join-Path $Package 'output') $RunName
Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') { throw 'R10EG requires develop' }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EG failed to read HEAD' }
    Write-Host "R10EG_BRANCH=$Branch"
    Write-Host "R10EG_HEAD=$Head"
    & git merge-base --is-ancestor '463880e69a4bf3a51b07654b74f3ac1c29798176' HEAD
    if ($LASTEXITCODE -ne 0) { throw 'R10EG requires reviewed R10EF ancestry' }
    $Blob = (& git rev-parse "HEAD:$Relative").Trim()
    if ($LASTEXITCODE -ne 0 -or $Blob -ne $ExpectedBlob) {
        throw 'R10EG transport source Git blob differs from reviewed source'
    }
    $TargetStatus = @(& git -c core.quotePath=false status --porcelain=v1 -- $Relative)
    if ($LASTEXITCODE -ne 0 -or $TargetStatus.Count -gt 0) {
        throw 'R10EG target has local changes, refusing to overwrite'
    }
    $Before = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EG initial Git status failed' }
    Write-Host "R10EG_EXISTING_TRACKED_CHANGES=$($Before.Count)"
    foreach ($line in $Before) { Write-Host "R10EG_PRESERVED_TRACKED=$line" }
    Write-Host 'R10EG_REVIEWED_SOURCE_AND_ANCESTRY=PASS'
    Write-Host 'R10EG_SCOPE=ONE_TYPED_ONE_STEM_PROPOSAL_GUARD'
    New-Item -Path $Output -ItemType Directory -Force | Out-Null
    $Original = [System.IO.File]::ReadAllBytes($Target)
    $AttemptedPatch = $true
    & python -B -m phase169_r10eg_one_stem_route_priority.patch $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EG guarded patch failed' }

    $Tests = @(
        '.\phase169_r10eg_one_stem_route_priority\tests\test_r10eg_patch.py',
        '.\phase169_r10eg_one_stem_route_priority\tests\test_r10eg_live.py',
        '.\phase169_r10e1_general_group_transport\tests\test_r10e1_general_transport.py',
        '.\phase169_r10ec_direct_sum_narrative_projection\tests\test_r10ec_projection.py',
        '.\phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py'
    )
    & python -B -m pytest -q -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R10EG focused pytest failed' }
    & python -B -m phase169_r10eg_one_stem_route_priority.audit $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EG one-stem focused audit failed' }

    $After = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EG final Git status failed' }
    $AfterOther = @($After | Where-Object { $_ -notmatch 'phase169_r10e1_general_group_transport/transport\.py$' })
    if (($Before -join "`n") -ne ($AfterOther -join "`n")) {
        Write-Host ('R10EG_TRACKED_BEFORE=' + ($Before -join ' || '))
        Write-Host ('R10EG_TRACKED_AFTER_OTHER=' + ($AfterOther -join ' || '))
        throw 'R10EG unrelated tracked status changed'
    }
    Write-Host 'R10EG_UNRELATED_TRACKED_FILES_UNCHANGED=PASS'
    Write-Host 'R10EG_INFERENCE_RULES_CHANGED=False'
    Write-Host 'R10EG_FULL_PYTEST_RUN=False'
    Write-Host 'R10EG_FOCUSED_TESTS_AND_TRUST=PASS'
    Write-Host "R10EG_OUTPUT=$Output"
    $Success = $true
}
catch {
    Write-Warning $_
    throw
}
finally {
    if (-not $Success -and $AttemptedPatch -and $null -ne $Original) {
        [System.IO.File]::WriteAllBytes($Target, $Original)
        Write-Host 'R10EG_ROLLBACK=transport source restored byte-for-byte'
    }
    Pop-Location
}
