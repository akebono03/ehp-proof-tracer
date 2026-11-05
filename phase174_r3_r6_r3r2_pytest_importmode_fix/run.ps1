param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $reviewedHead = 'ecbb2fea225c5b88000629d9c025934fcc2d7075'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R3-R6-R3R2 requires develop.'
    }
    git fetch origin
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify origin/develop.' }
    $localHead = (git rev-parse HEAD).Trim()
    $remoteHead = (git rev-parse origin/develop).Trim()
    if ($LASTEXITCODE -ne 0 -or $localHead -ne $reviewedHead -or $remoteHead -ne $reviewedHead) {
        throw "Unreviewed HEAD: local=$localHead remote=$remoteHead reviewed=$reviewedHead"
    }
    Write-Output "PHASE174_R3R6R3R2_BRANCH=$branch"
    Write-Output "PHASE174_R3R6R3R2_LOCAL_HEAD=$localHead"
    Write-Output "PHASE174_R3R6R3R2_REMOTE_HEAD=$remoteHead"

    # This is a check, not the earlier --apply operation.  The prior apply
    # already succeeded and must not be run a second time.
    python -m phase174_r3_r6_r3r2_pytest_importmode_fix.verify
    if ($LASTEXITCODE -ne 0) {
        throw 'Previously applied common Renderer differs from reviewed implementation.'
    }

    $testFiles = @(
        'phase174_r3_r6_r3r2_pytest_importmode_fix/tests/test_r3r2_importmode.py',
        'phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py',
        'phase174_r3_r6_r3_common_narrative/tests/test_projection.py',
        'phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py',
        'phase174_r3_r6_source_extension/tests/test_source.py',
        'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
        'phase172_r5_prior_reference_display/tests/test_projection.py'
    )
    foreach ($testFile in $testFiles) {
        if (-not (Test-Path $testFile -PathType Leaf)) {
            throw "Missing focused test file: $testFile"
        }
    }
    Write-Output 'PHASE174_R3R6R3R2_PYTEST_IMPORT_MODE=importlib'
    Write-Output "PHASE174_R3R6R3R2_FOCUSED_TEST_FILES=$($testFiles.Count)"

    $pytestArgs = @('-q', '--import-mode=importlib', '-p', 'no:cacheprovider')
    if ($DryRun) {
        $pytestArgs += '--collect-only'
        Write-Output 'PHASE174_R3R6R3R2_COLLECTION_START'
    } else {
        Write-Output 'PHASE174_R3R6R3R2_FOCUSED_PYTEST_START'
    }
    $pytestArgs += $testFiles
    python -m pytest @pytestArgs
    if ($LASTEXITCODE -ne 0) {
        if ($DryRun) {
            throw 'R3R2 test collection failed; no production changes made.'
        }
        throw 'R3R2 focused pytest failed; Gate not certified.'
    }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R6R3R2_COLLECTION=PASS'
        Write-Output 'PHASE174_R3R6R3R2_DRY_RUN=PASS'
    } else {
        Write-Output 'PHASE174_R3R6R3R2_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE174_R3R6R3R2_GATE=PASS'
    }
} finally {
    Pop-Location
}
