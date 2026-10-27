$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$passed = $false
$staged = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
$baseDb = Join-Path $root 'phase169_r10e4_ordered_db_prior/db_prior.py'
$beforeDb = Join-Path $folder 'output/db_prior.py.before'
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    $head = (git rev-parse HEAD).Trim()
    if ($branch -ne 'develop' -or $head -ne '7a687a58443d1cfe40ba03923dd9be60fa462788') {
        throw 'R10E4R4 requires reviewed develop HEAD 7a687a5.'
    }
    Write-Host "R10E4R4_BRANCH=$branch"
    Write-Host "R10E4R4_HEAD=$head"
    $required = Join-Path $root 'phase169_r10e4r2_explicit_db_row_parser/run.ps1'
    if (-not (Test-Path $required)) { throw 'R10E4R4 requires installed R10E4R2 runner.' }
    $runnerText = [System.IO.File]::ReadAllText($required)
    if ($runnerText.Contains("Replace('','/')")) {
        throw 'R10E4R4 requires the previously installed R10E4R3 PowerShell repair.'
    }
    if (-not (Test-Path $baseDb)) { throw 'R10E4R4 missing R10E4 db_prior.py.' }
    New-Item -ItemType Directory -Path (Join-Path $folder 'output') -Force | Out-Null
    [System.IO.File]::WriteAllBytes($beforeDb, [System.IO.File]::ReadAllBytes($baseDb))
    $trackedBefore = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | Sort-Object -Unique)
    $staged = $true
    python -m phase169_r10e4r4_db_prior_test_alignment.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R4 failed to stage test and parser fixes.' }
    # Reuse the established R10E4R2 production-only patch, regression suite,
    # audit, and its independent rollback path.
    & powershell -NoProfile -ExecutionPolicy Bypass -File $required
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R4 parent R10E4R2 verification failed.' }
    python -m pytest -q (Join-Path $folder 'tests/test_r10e4r4_explicit_rows.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E4R4 new fail-closed tests failed.' }
    $trackedAfter = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | Sort-Object -Unique)
    $allowed = @(
        'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py',
        'phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py'
    )
    $unexpected = @($trackedAfter | Where-Object { ($trackedBefore -notcontains $_) -and ($allowed -notcontains $_) })
    $removed = @($trackedBefore | Where-Object { $trackedAfter -notcontains $_ })
    Write-Host ('R10E4R4_UNEXPECTED_TRACKED=' + ($unexpected -join '|'))
    Write-Host ('R10E4R4_REMOVED_TRACKED=' + ($removed -join '|'))
    if ($unexpected.Count -gt 0 -or $removed.Count -gt 0) {
        throw 'R10E4R4 tracked file integrity check failed.'
    }
    $passed = $true
    Write-Host 'R10E4R4_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E4R4_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10E4R4_PRODUCTION_FILES_CHANGED=phase169_r10e4_ordered_db_prior/db_prior.py'
    Write-Host 'R10E4R4_HISTORICAL_TESTS_UPDATED=R10E1,R10E2'
    Write-Host 'R10E4R4_FULL_PYTEST_RUN=False'
} finally {
    if ($staged -and -not $passed) {
        if (Test-Path $beforeDb) {
            [System.IO.File]::WriteAllBytes($baseDb, [System.IO.File]::ReadAllBytes($beforeDb))
        }
        foreach ($file in @(
            'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py',
            'phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py',
            'phase169_r10e4r2_explicit_db_row_parser/_has_explicit_row_FULL.py'
        )) {
            $backup = Join-Path $folder ('output/' + $file.Replace('/','__') + '.before')
            $dest = Join-Path $root $file
            if (Test-Path $backup) {
                [System.IO.File]::WriteAllBytes($dest, [System.IO.File]::ReadAllBytes($backup))
            }
        }
        Write-Host 'R10E4R4_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
