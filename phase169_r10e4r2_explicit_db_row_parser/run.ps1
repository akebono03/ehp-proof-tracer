$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$relative = 'phase169_r10e4_ordered_db_prior/db_prior.py'
$target = Join-Path $root $relative
$backup = Join-Path $folder 'output/db_prior.py.before'
$changed = $false
$passed = $false
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E4R2 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R2 failed to read git HEAD.' }
    Write-Host "R10E4R2_BRANCH=$branch"
    Write-Host "R10E4R2_HEAD=$head"
    if (-not (Test-Path $target)) { throw 'R10E4R2 missing R10E4 installed DB module.' }
    foreach ($required in @('data/sphere.csv','data/HyoujiGen.csv','phase169_r10e4_ordered_db_prior/audit.py')) {
        if (-not (Test-Path (Join-Path $root $required))) { throw "R10E4R2 missing: $required" }
    }
    $beforeTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R2 cannot read tracked changes.' }
    New-Item -ItemType Directory -Path (Join-Path $folder 'output') -Force | Out-Null
    [System.IO.File]::WriteAllBytes($backup, [System.IO.File]::ReadAllBytes($target))
    $changed = $true
    python -m phase169_r10e4r2_explicit_db_row_parser.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R2 guarded patch failed.' }
    python -m pytest -q `
        (Join-Path $folder 'tests/test_r10e4r2_db_separators.py') `
        (Join-Path $root 'phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py') `
        (Join-Path $root 'phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py') `
        (Join-Path $root 'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport/tests/test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py') `
        (Join-Path $root 'phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py') `
        (Join-Path $root 'phase168_r3_41p19_phase_closeout/tests/test_phase168_r3_41p19_phase_closeout.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R2 limited pytest failed.' }
    python -m phase169_r10e4r2_explicit_db_row_parser.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R2 focused audit failed.' }
    $afterTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R2 cannot read final tracked changes.' }
    $added = @($afterTracked | Where-Object { $beforeTracked -notcontains $_ })
    $removed = @($beforeTracked | Where-Object { $afterTracked -notcontains $_ })
    Write-Host ('R10E4R2_TRACKED_ADDED=' + ($added -join '|'))
    Write-Host ('R10E4R2_TRACKED_REMOVED=' + ($removed -join '|'))
    if ($added.Count -ne 0 -or $removed.Count -ne 0) { throw 'R10E4R2 unrelated tracked files were modified.' }
    $before = [System.IO.File]::ReadAllBytes($backup)
    $after = [System.IO.File]::ReadAllBytes($target)
    if ([Convert]::ToBase64String($before) -eq [Convert]::ToBase64String($after)) { throw 'R10E4R2 expected a changed module.' }
    $passed = $true
    Write-Host 'R10E4R2_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E4R2_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10E4R2_PRODUCTION_FILES_CHANGED=phase169_r10e4_ordered_db_prior/db_prior.py'
    Write-Host 'R10E4R2_FULL_PYTEST_RUN=False'
} finally {
    if ($changed -and -not $passed) {
        if (Test-Path $backup) { [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup)) }
        Write-Host 'R10E4R2_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
