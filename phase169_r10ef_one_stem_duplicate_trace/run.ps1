$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Output = Join-Path $Package 'output'
New-Item -ItemType Directory -Path $Output -Force | Out-Null
Push-Location $Repo
try {
    $branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git branch failed' }
    $head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git rev-parse failed' }
    Write-Host "R10EF_BRANCH=$branch"
    Write-Host "R10EF_HEAD=$head"
    if ($branch -ne 'develop') {
        throw 'R10EF requires local develop; no checkout or reset is performed'
    }
    & git merge-base --is-ancestor '0cb9b8a88823ccd94a4a8967997bb302d98668eb' HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'R10EF requires the reviewed R10EC-R1 ancestor'
    }
    $expected = [ordered]@{
        'phase165_r3_recursive_search.py' = '9c424f61a2b4a2d7789777017ad4f91292b0ad30'
        'phase165_r6_2_r4_r8_dedup.py' = '48e563251e512c25559027139b51825dc655195a'
        'phase165_r55_nk_only_goal.py' = 'b207b8169590e634229d412324d857ffb3857939'
        'phase165_r52_r9_shared_math.py' = 'd015e11030a15a62fbe75099bda10ddacdfdcbc5'
        'phase168_r3_41p13_trust_boundary/verification.py' = '547464846ce574d227092a4aacb895d2e2dfefca'
    }
    foreach ($path in $expected.Keys) {
        $blob = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $expected[$path]) {
            throw "R10EF unreviewed tracked Git blob: $path"
        }
    }
    Write-Host 'R10EF_REVIEWED_DEPENDENCIES=PASS'
    Write-Host 'R10EF_SCOPE=AUDIT_ONLY'

    # Capture BOTH the previously existing tracked status and the final status.
    # This resolves the opaque R10EE guard failure without resetting any file.
    $before = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EF git status before failed' }
    $beforeFile = Join-Path $Output 'tracked_status_before.txt'
    [System.IO.File]::WriteAllLines($beforeFile, [string[]]$before)
    Write-Host "R10EF_TRACKED_BEFORE_COUNT=$($before.Count)"
    foreach ($line in $before) { Write-Host "R10EF_TRACKED_BEFORE=$line" }

    & python -B -m pytest -q '.\phase169_r10ef_one_stem_duplicate_trace\tests\test_r10ef_trace.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EF focused tests failed' }
    & python -B -m phase169_r10ef_one_stem_duplicate_trace.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10EF root derivation audit failed' }

    $after = @(& git -c core.quotePath=false status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EF git status after failed' }
    $afterFile = Join-Path $Output 'tracked_status_after.txt'
    [System.IO.File]::WriteAllLines($afterFile, [string[]]$after)
    Write-Host "R10EF_TRACKED_AFTER_COUNT=$($after.Count)"
    foreach ($line in $after) { Write-Host "R10EF_TRACKED_AFTER=$line" }
    $statusChanged = ($before -join "`n") -ne ($after -join "`n")
    if ($statusChanged) {
        $added = @(Compare-Object -ReferenceObject ([string[]](@("<BEGIN>") + $before + @("<END>"))) -DifferenceObject ([string[]](@("<BEGIN>") + $after + @("<END>"))))
        Write-Host 'R10EF_TRACKED_STATUS_CHANGED=True'
        foreach ($item in $added) {
            Write-Host "R10EF_TRACKED_DIFF=$($item.SideIndicator) $($item.InputObject)"
        }
        throw 'R10EF tracked status changed; inspect printed paths (no reset performed)'
    }
    Write-Host 'R10EF_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Host 'R10EF_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10EF_PROOF_RULES_CHANGED=False'
    Write-Host 'R10EF_FULL_PYTEST_RUN=False'
    Write-Host 'R10EF_FOCUSED_TESTS_AND_TRACE=PASS'
}
finally {
    Pop-Location
}
