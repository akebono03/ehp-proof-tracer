$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
$phase = 'phase169_r10er_r1_mixed_definition_projection'
$target = 'phase169_r10ec_direct_sum_narrative_projection/projection.py'
$allowed = @(
    '3e102f43b5d378d511391e0b3eb5a175f07ac2dc',
    'ff2fc98d1245839d62817eac409f32d302c7083a'
)
$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
Write-Host "R10ER_BRANCH=$branch"
Write-Host "R10ER_HEAD=$head"
if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop' -or $head -notin $allowed) {
    throw 'Only reviewed develop HEADs are supported; no files changed.'
}
if (-not (Test-Path (Join-Path $root "$phase\patch.py"))) {
    throw 'Run from repository root after extracting the ZIP.'
}
$initial = @(& git diff --name-only HEAD -- $target)
if ($LASTEXITCODE -ne 0 -or $initial.Count -ne 0) {
    throw 'Projection already modified; refusing overwrite.'
}
$before = @(& git diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0) { throw 'Initial git diff failed.' }
Write-Host "R10ER_PREEXISTING_TRACKED_DIFF=$($before -join ',')"
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss_ffff'
$out = Join-Path $root "$phase\output\run_$stamp"
New-Item -Path $out -ItemType Directory -Force | Out-Null
try {
    Write-Host 'R10ER_PATCH_START'
    & python -m phase169_r10er_r1_mixed_definition_projection.patch $out
    if ($LASTEXITCODE -ne 0) { throw 'Exact-source patch failed' }
    Write-Host 'R10ER_LIMITED_TEST_START'
    & python -m pytest -q -p no:cacheprovider `
        "$phase/tests/test_r10er_projection.py" `
        "$phase/tests/test_r10er_static.py" `
        'phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py' `
        'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py' `
        'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_live.py' `
        'phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py'
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
    Write-Host 'R10ER_LIVE_AUDIT_START'
    & python -m phase169_r10er_r1_mixed_definition_projection.audit (Join-Path $out 'audit')
    if ($LASTEXITCODE -ne 0) { throw 'Live audit failed' }
    $after = @(& git diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0) { throw 'Final git diff failed' }
    $expected = @($before + @($target) | Sort-Object -Unique)
    $actual = @($after | Sort-Object -Unique)
    if (($expected -join '|') -ne ($actual -join '|')) {
        Write-Host "R10ER_EXPECTED_TRACKED=$($expected -join ',')"
        Write-Host "R10ER_ACTUAL_TRACKED=$($actual -join ',')"
        throw 'Unexpected tracked changes'
    }
    Write-Host "R10ER_EXPECTED_PRODUCTION_FILE=$target"
    Write-Host 'R10ER_FULL_TEST_RUN=False'
    Write-Host "R10ER_OUTPUT=$out"
    Write-Host 'R10ER_COMPLETE=PASS'
}
catch {
    Write-Host "R10ER_FAILURE=$($_.Exception.Message)"
    $backup = Join-Path $out 'projection.py.before'
    if (Test-Path $backup) {
        Copy-Item -LiteralPath $backup -Destination (Join-Path $root $target) -Force
        Write-Host "R10ER_RESTORED=$target"
    }
    throw
}
