$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$relative = 'phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py'
$target = Join-Path $root $relative
$backup = Join-Path $folder 'output/test_r10e2_unpositioned_citation.py.before'
$changed = $false
$passed = $false
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E4R1 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R1 cannot read HEAD.' }
    Write-Host "R10E4R1_BRANCH=$branch"
    Write-Host "R10E4R1_HEAD=$head"
    if (-not (Test-Path $target)) { throw 'R10E4R1 historical test missing.' }
    $required = Join-Path $root 'phase169_r10e4_ordered_db_prior/run.ps1'
    if (-not (Test-Path $required)) { throw 'R10E4R1 original R10E4 run.ps1 missing.' }
    git diff --quiet HEAD -- $relative
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R1 historical test has user edits; refusing overwrite.' }
    $expectedTargets = @(
        'phase165_r3_recursive_search.py',
        'phase168_r3_41p13_trust_boundary/verification.py',
        'phase169_r10e1_general_group_transport/transport.py'
    )
    foreach ($name in $expectedTargets) {
        git diff --quiet HEAD -- $name
        if ($LASTEXITCODE -ne 0) { throw "R10E4R1 production target already modified: $name" }
    }
    New-Item -ItemType Directory -Force -Path (Join-Path $folder 'output') | Out-Null
    [System.IO.File]::WriteAllBytes($backup, [System.IO.File]::ReadAllBytes($target))
    $changed = $true
    python -m phase169_r10e4r1_historical_test_compatibility.patch_test
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R1 guarded test patch failed.' }
    python -m pytest -q (Join-Path $folder 'tests/test_r10e4r1_historical_test_update.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R1 migration tests failed.' }
    powershell -NoProfile -ExecutionPolicy Bypass -File $required
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R1 underlying R10E4 run failed.' }
    $current = [System.IO.File]::ReadAllBytes($target)
    $original = [System.IO.File]::ReadAllBytes($backup)
    if ([Convert]::ToBase64String($current) -eq [Convert]::ToBase64String($original)) {
        throw 'R10E4R1 expected updated historical test.'
    }
    $passed = $true
    Write-Host 'R10E4R1_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E4R1_PRODUCTION_PATCHED_BY=R10E4'
    Write-Host 'R10E4R1_HISTORICAL_TEST_COMPATIBILITY=PASS'
    Write-Host 'R10E4R1_FULL_PYTEST_RUN=False'
} finally {
    if ($changed -and -not $passed) {
        if (Test-Path $backup) {
            [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        }
        Write-Host 'R10E4R1_HISTORICAL_TEST_ROLLBACK=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
