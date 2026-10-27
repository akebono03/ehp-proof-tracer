$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = (Resolve-Path (Join-Path $here '..')).Path
$targetRel = 'phase165_r52_r9_shared_math.py'
$target = Join-Path $root $targetRel
$backup = Join-Path $here 'output/phase165_r52_r9_shared_math.py.before'
$success = $false
$patchAttempted = $false
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    $head = (git rev-parse HEAD).Trim()
    Write-Host "R10E5_BRANCH=$branch"
    Write-Host "R10E5_HEAD=$head"
    if ($branch -ne 'develop' -or $head -ne 'd6c4bd745b2537ffe4da72a7a77865d3c00f6e18') {
        throw 'R10E5R1 requires the reviewed develop HEAD d6c4bd7.'
    }
    if (-not (Test-Path (Join-Path $root 'phase169_r10e4_ordered_db_prior/db_prior.py'))) {
        throw 'R10E5 requires previously installed R10E4 database prior policy.'
    }
    if (-not (Test-Path (Join-Path $root 'phase169_r10e4r4_db_prior_test_alignment/tests'))) {
        throw 'R10E5 requires completed R10E4-R4 regression tests.'
    }
    $trackBefore = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    $otherBefore = @($trackBefore | Where-Object { $_ -ne $targetRel })
    Write-Host ('R10E5_EXISTING_TRACKED=' + ($trackBefore -join '|'))
    if ($trackBefore -contains $targetRel) {
        throw 'R10E5R1 refuses to overwrite pre-existing tracked edits to production target.'
    }
    $reviewedBlob = 'd56c0a8dac49fb3abf285ff371bd7336966d9715'
    $currentBlob = (git rev-parse "HEAD:$targetRel").Trim()
    if ($LASTEXITCODE -ne 0 -or $currentBlob -ne $reviewedBlob) {
        throw 'R10E5R1 production source blob differs from reviewed develop.'
    }
    Write-Host 'R10E5R1_REVIEWED_PRODUCTION_BLOB=PASS'
    $patchAttempted = $true
    python -m phase169_r10e5_composite_generator_image.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E5 guarded patch failed.' }
    $focused = @(
        'phase169_r10e5_composite_generator_image/tests',
        'phase169_r10e4_ordered_db_prior/tests',
        'phase169_r10e4r2_explicit_db_row_parser/tests',
        'phase169_r10e4r4_db_prior_test_alignment/tests',
        'phase169_r10e1_general_group_transport/tests',
        'phase169_r10e2_unpositioned_citation/tests',
        'phase169_r10d2_general_family_definition/tests',
        'phase169_r10b_registered_stable_family_binding/tests',
        'phase169_r7_general_stable_transport/tests',
        'phase168_r3_41p13_trust_boundary/tests',
        'phase168_r3_41p19_phase_closeout/tests'
    )
    python -m pytest -q @focused
    if ($LASTEXITCODE -ne 0) { throw 'R10E5 focused pytest failed.' }
    python -m phase169_r10e5_composite_generator_image.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E5 audit failed.' }
    $trackAfter = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    $otherAfter = @($trackAfter | Where-Object { $_ -ne $targetRel })
    $added = @($otherAfter | Where-Object { $otherBefore -notcontains $_ })
    $removed = @($otherBefore | Where-Object { $otherAfter -notcontains $_ })
    Write-Host ('R10E5_UNRELATED_ADDED=' + ($added -join '|'))
    Write-Host ('R10E5_UNRELATED_REMOVED=' + ($removed -join '|'))
    if ($added.Count -gt 0 -or $removed.Count -gt 0) {
        throw 'R10E5 unrelated tracked changes detected.'
    }
    if ((-not (Test-Path $backup)) -or
        ((Get-FileHash -Path $backup -Algorithm SHA256).Hash -eq
         (Get-FileHash -Path $target -Algorithm SHA256).Hash)) {
        throw 'R10E5 production target was not modified.'
    }
    $success = $true
    Write-Host 'R10E5_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E5_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host ('R10E5_PRODUCTION_FILES_CHANGED=' + $targetRel)
    Write-Host 'R10E5_FULL_PYTEST_RUN=False'
    Write-Host 'R10E5R1_HEAD_GUARD_RESULT=PASS'
} finally {
    if ($patchAttempted -and -not $success -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10E5_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
