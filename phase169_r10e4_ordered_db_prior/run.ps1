$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$targets = @(
    'phase165_r3_recursive_search.py',
    'phase168_r3_41p13_trust_boundary/verification.py',
    'phase169_r10e1_general_group_transport/transport.py'
)
$patched = $false
$passed = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E4 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E4 cannot read Git HEAD.' }
    Write-Host "R10E4_BRANCH=$branch"
    Write-Host "R10E4_HEAD=$head"
    $required = @(
        'phase169_r10e2_unpositioned_citation/source_first.py',
        'phase169_r10e1_general_group_transport/transport.py',
        'phase169_r10d2_general_family_definition/family_citation.py',
        'data/sphere.csv',
        'data/HyoujiGen.csv'
    )
    foreach ($item in $required) {
        if (-not (Test-Path (Join-Path $root $item))) { throw "R10E4 missing prerequisite: $item" }
    }
    $beforeTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { throw 'R10E4 cannot read initial tracked diff.' }
    $beforeOther = @($beforeTracked | Where-Object { $targets -notcontains $_ })
    Write-Host ('R10E4_EXISTING_TRACKED=' + ($beforeTracked -join '|'))
    # Record the exact pre-run bytes before any guard can fail.
    $outputDir = Join-Path $folder 'output'
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    foreach ($target in $targets) {
        $from = Join-Path $root $target
        $backup = Join-Path $outputDir ([System.IO.Path]::GetFileName($target) + '.before')
        [System.IO.File]::WriteAllBytes($backup, [System.IO.File]::ReadAllBytes($from))
    }
    $patched = $true
    python -m phase169_r10e4_ordered_db_prior.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E4 guarded patch failed.' }
    python -m pytest -q `
        (Join-Path $folder 'tests/test_r10e4_ordered_db_prior.py') `
        (Join-Path $root 'phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py') `
        (Join-Path $root 'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport/tests/test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py') `
        (Join-Path $root 'phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py') `
        (Join-Path $root 'phase168_r3_41p19_phase_closeout/tests/test_phase168_r3_41p19_phase_closeout.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E4 focused pytest failed.' }
    python -m phase169_r10e4_ordered_db_prior.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E4 audit failed.' }
    $afterTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { throw 'R10E4 cannot read final tracked diff.' }
    $afterOther = @($afterTracked | Where-Object { $targets -notcontains $_ })
    $added = @($afterOther | Where-Object { $beforeOther -notcontains $_ })
    $removed = @($beforeOther | Where-Object { $afterOther -notcontains $_ })
    Write-Host ('R10E4_UNRELATED_ADDED=' + ($added -join '|'))
    Write-Host ('R10E4_UNRELATED_REMOVED=' + ($removed -join '|'))
    if ($added.Count -gt 0 -or $removed.Count -gt 0) {
        throw 'R10E4 detected unrelated tracked changes.'
    }
    foreach ($target in $targets) {
        $backup = Join-Path $folder ('output/' + [System.IO.Path]::GetFileName($target) + '.before')
        if (-not (Test-Path $backup)) { throw "R10E4 missing backup: $target" }
        $original = [System.IO.File]::ReadAllBytes($backup)
        $changed = [System.IO.File]::ReadAllBytes((Join-Path $root $target))
        if ([Convert]::ToBase64String($original) -eq [Convert]::ToBase64String($changed)) {
            throw "R10E4 patch target unchanged: $target"
        }
    }
    $passed = $true
    Write-Host 'R10E4_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E4_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host ('R10E4_PRODUCTION_FILES_CHANGED=' + ($targets -join ','))
    Write-Host 'R10E4_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed) {
        foreach ($target in $targets) {
            $backup = Join-Path $folder ('output/' + [System.IO.Path]::GetFileName($target) + '.before')
            if (Test-Path $backup) {
                [System.IO.File]::WriteAllBytes((Join-Path $root $target), [System.IO.File]::ReadAllBytes($backup))
            }
        }
        Write-Host 'R10E4_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
