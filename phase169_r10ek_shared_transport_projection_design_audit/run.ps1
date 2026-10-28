$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$TimeStamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Package "output\run_$TimeStamp"
New-Item -ItemType Directory -Force -Path $Output | Out-Null
Push-Location $Repo
try {
    $branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git branch failed' }
    $head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git rev-parse failed' }
    Write-Host "R10EK_BRANCH=$branch"
    Write-Host "R10EK_HEAD=$head"
    Write-Host 'R10EK_MODE=AUDIT_ONLY'
    if ($branch -ne 'develop') { throw 'R10EK requires local develop; no checkout or reset is performed' }
    & git merge-base --is-ancestor '01e20c4d7bb74b8680bd3311130358266c97e884' HEAD
    if ($LASTEXITCODE -ne 0) { throw 'R10EK requires reviewed R10EJ predecessor commit' }
    $expected = @{
        'phase169_r10ec_direct_sum_narrative_projection/projection.py' = 'ace11ebd4841ac81592ef4f948507e63bc9f6038'
        'phase168_r3_5_model_renderer.py' = '2685ef3ef6bf7bc1673dededef1e3487d9941362'
    }
    foreach ($relative in $expected.Keys) {
        $observed = (& git hash-object -- $relative).Trim()
        if ($LASTEXITCODE -ne 0 -or $observed -ne $expected[$relative]) {
            throw "R10EK reviewed source differs: $relative ($observed)"
        }
    }
    $cyclicFile = Join-Path $Repo 'phase169_r10a_verified_stable_chain_projection/projection.py'
    $cyclicHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $cyclicFile).Hash.ToLowerInvariant()
    $expectedCyclicHash = '60aa71eebac2441c8b1f51f8636f7c8b63b1c51eaacc744132e84d7098fb9864'
    if ($cyclicHash -ne $expectedCyclicHash) {
        throw "R10EK expects the reviewed R10EJ cyclic projection; found $cyclicHash"
    }
    Write-Host 'R10EK_SOURCE_CONTRACT=REVIEWED_R10EJ_AND_R10EC'
    $before = @(& git -c core.quotepath=false status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'git status before failed' }
    Write-Host "R10EK_TRACKED_BEFORE_COUNT=$($before.Count)"
    $oldDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE
    $env:PYTHONDONTWRITEBYTECODE = '1'
    try {
        & python -B -m pytest -q -p no:cacheprovider '.\phase169_r10ek_shared_transport_projection_design_audit\tests\test_r10ek_contract.py'
        if ($LASTEXITCODE -ne 0) { throw 'R10EK focused contract tests failed' }
        & python -B -m phase169_r10ek_shared_transport_projection_design_audit.audit $Output
        if ($LASTEXITCODE -ne 0) { throw 'R10EK real-proof shared contract audit failed' }
    }
    finally {
        $env:PYTHONDONTWRITEBYTECODE = $oldDontWriteBytecode
    }
    $after = @(& git -c core.quotepath=false status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'git status after failed' }
    if (@(Compare-Object -ReferenceObject $before -DifferenceObject $after).Count -ne 0) {
        Write-Host "R10EK_TRACKED_BEFORE=$($before -join '; ')"
        Write-Host "R10EK_TRACKED_AFTER=$($after -join '; ')"
        throw 'R10EK unexpectedly changed tracked file status'
    }
    Write-Host 'R10EK_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Host 'R10EK_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10EK_FULL_PYTEST_RUN=False'
    Write-Host 'R10EK_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host "R10EK_OUTPUT=$Output"
}
finally {
    Pop-Location
}
