$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = (Resolve-Path (Join-Path $here '..')).Path
$targetRel = 'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py'
$target = Join-Path $root $targetRel
$backup = Join-Path $here 'output/test_r10e5_composite_generator_image.py.before'
$child = Join-Path $root 'phase169_r10e5_composite_generator_image/run.ps1'
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
    Write-Host "R10E5R3_BRANCH=$branch"
    Write-Host "R10E5R3_HEAD=$head"
    if ($branch -ne 'develop' -or $head -ne 'd6c4bd745b2537ffe4da72a7a77865d3c00f6e18') {
        throw 'R10E5R3 requires reviewed develop HEAD d6c4bd7.'
    }
    if (-not (Test-Path $target) -or -not (Test-Path $child)) {
        throw 'R10E5R3 requires previously extracted R10E5-R2 package.'
    }
    # Never overwrite unrelated tracked edits; child runner owns production rollback.
    $beforeTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' })
    Write-Host ('R10E5R3_EXISTING_TRACKED=' + ($beforeTracked -join '|'))
    $patchAttempted = $true
    python -m phase169_r10e5r3_match_order_test_fix.patch_test
    if ($LASTEXITCODE -ne 0) { throw 'R10E5R3 guarded test patch failed.' }
    python -m pytest -q 'phase169_r10e5r3_match_order_test_fix/tests'
    if ($LASTEXITCODE -ne 0) { throw 'R10E5R3 targeted patch verification failed.' }
    & powershell -ExecutionPolicy Bypass -File $child
    if ($LASTEXITCODE -ne 0) { throw 'R10E5R3 parent R10E5 focused pytest/audit failed.' }
    $afterTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' })
    $unexpected = @($afterTracked | Where-Object { $beforeTracked -notcontains $_ -and $_ -ne 'phase165_r52_r9_shared_math.py' })
    $missing = @($beforeTracked | Where-Object { $afterTracked -notcontains $_ })
    Write-Host ('R10E5R3_UNEXPECTED_TRACKED=' + ($unexpected -join '|'))
    Write-Host ('R10E5R3_MISSING_TRACKED=' + ($missing -join '|'))
    if ($unexpected.Count -gt 0 -or $missing.Count -gt 0) {
        throw 'R10E5R3 unrelated tracked changes detected.'
    }
    $success = $true
    Write-Host 'R10E5R3_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E5R3_FOCUSED_TEST_AND_AUDIT=PASS'
    Write-Host 'R10E5R3_TEST_FILES_CHANGED=phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py'
    Write-Host 'R10E5R3_FULL_PYTEST_RUN=False'
} finally {
    if ($patchAttempted -and -not $success -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10E5R3_TEST_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
