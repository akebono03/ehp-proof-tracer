$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
$phase = 'phase169_r10eq_r1_universal_stable_definition'
$target = 'phase165_r52_r9_shared_math.py'
$expected = '3e102f43b5d378d511391e0b3eb5a175f07ac2dc'
$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
Write-Host "R10EQ_BRANCH=$branch"
Write-Host "R10EQ_HEAD=$head"
if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop' -or $head -ne $expected) {
    throw 'Expected exact inspected develop HEAD; nothing patched.'
}
if (-not (Test-Path (Join-Path $root "$phase\definition.py"))) {
    throw 'Run from the repository root after extracting the ZIP.'
}
$initialTarget = @(& git diff --name-only HEAD -- $target)
if ($LASTEXITCODE -ne 0 -or $initialTarget.Count -ne 0) {
    throw 'Shared provider already has tracked modifications; refusing to overwrite.'
}
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss_ffff'
$out = Join-Path $root "$phase\output\run_$stamp"
New-Item -Path $out -ItemType Directory -Force | Out-Null
$patched = $false
try {
    Write-Host 'R10EQ_SOURCE_PATCH_START'
    & python -m phase169_r10eq_r1_universal_stable_definition.patch $out
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    $patched = $true
    Write-Host 'R10EQ_LIMITED_TEST_START'
    & python -m pytest -q -p no:cacheprovider `
        "$phase/tests/test_r10eq_stable_definition.py" `
        "$phase/tests/test_r10eq_live.py" `
        'phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py' `
        'phase169_r10eo_r3_reviewed_definition_bridge/tests/test_r10eo_r3_definition_bridge.py' `
        'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py' `
        'phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py'
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
    Write-Host 'R10EQ_LIVE_AUDIT_START'
    & python -m phase169_r10eq_r1_universal_stable_definition.audit (Join-Path $out 'audit')
    if ($LASTEXITCODE -ne 0) { throw 'Live audit failed' }
    $tracked = @(& git diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0) { throw 'git diff failed' }
    $unexpected = @($tracked | Where-Object { $_ -ne $target })
    if ($unexpected.Count -ne 0) {
        Write-Host "R10EQ_UNEXPECTED_TRACKED=$($unexpected -join ',')"
        throw 'Tracked unrelated files changed'
    }
    Write-Host "R10EQ_EXPECTED_PRODUCTION_FILE=$target"
    Write-Host 'R10EQ_FULL_TEST_RUN=False'
    Write-Host "R10EQ_OUTPUT=$out"
    Write-Host 'R10EQ_COMPLETE=PASS'
}
catch {
    Write-Host "R10EQ_FAILURE=$($_.Exception.Message)"
    $backup = Join-Path $out 'shared_math.py.before'
    if (Test-Path $backup) {
        Copy-Item -LiteralPath $backup -Destination (Join-Path $root $target) -Force
        Write-Host "R10EQ_RESTORED=$target"
    }
    throw
}
