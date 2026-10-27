$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$backupFolder = Join-Path $folder 'output'
$targets = @(
    'phase165_r52_r9_shared_math.py',
    'phase165_r55_nk_only_goal.py',
    'web_group_proof.py',
    'phase168_r3_41p13_trust_boundary/verification.py',
    'phase169_r10e1_general_group_transport/transport.py',
    'phase168_r3_5_model_renderer.py'
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
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E2R3 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R3 failed to inspect HEAD.' }
    Write-Host "R10E2R3_BRANCH=$branch"
    Write-Host "R10E2R3_HEAD=$head"
    $required = @(
        'phase169_r10e1_general_group_transport/transport.py',
        'phase169_r10d2_general_family_definition/family_citation.py',
        'phase169_r10b_registered_stable_family_binding/family_registry.py',
        'data/HyoujiGen.csv'
    )
    foreach ($item in $required) {
        if (-not (Test-Path (Join-Path $root $item))) {
            throw "R10E2R3 missing prerequisite: $item"
        }
    }
    # Read the complete Git result first, then exclude the six approved
    # patch targets in PowerShell. The previous Git pathspec exclusions
    # were ineffective and classified all six approved files as unrelated.
    $beforeTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . |
        Where-Object { $_ -ne '' } |
        ForEach-Object { $_.Replace('\', '/') } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R3 cannot inspect tracked files.' }
    $beforeTargets = @($beforeTracked | Where-Object { $targets -contains $_ })
    $beforeOther = @($beforeTracked | Where-Object { $targets -notcontains $_ })
    Write-Host ('R10E2R3_TRACKED_BEFORE=' + ($beforeTracked -join '|'))
    Write-Host ('R10E2R3_UNRELATED_BEFORE=' + ($beforeOther -join '|'))
    if ($beforeTargets.Count -gt 0) {
        throw ('R10E2R3 refuses to overwrite pre-existing tracked edits in patch targets: ' +
            ($beforeTargets -join '|'))
    }
    # Verify the exclusion predicate used below, before patching any files.
    $filterProbe = @($targets[0], 'unrelated-file.test')
    $probeOther = @($filterProbe | Where-Object { $targets -notcontains $_ })
    if ($probeOther.Count -ne 1 -or $probeOther[0] -ne 'unrelated-file.test') {
        throw 'R10E2R3 target-exclusion filter failed its self-check.'
    }
    python -m phase169_r10e2_unpositioned_citation.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R3 guarded production patch failed.' }
    $patched = $true
    python -m pytest -q `
        (Join-Path $folder 'tests/test_r10e2_unpositioned_citation.py') `
        (Join-Path $root 'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport/tests/test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py') `
        (Join-Path $root 'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py') `
        (Join-Path $root 'phase169_r10a2_unified_one_stem/tests/test_r10a2_one_stem_projection.py') `
        (Join-Path $root 'phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py') `
        (Join-Path $root 'phase168_r3_41p15_complete_fail_closed/tests/test_phase168_r3_41p15_complete_fail_closed.py') `
        (Join-Path $root 'phase168_r3_41p19_phase_closeout/tests/test_phase168_r3_41p19_phase_closeout.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R3 focused pytest failed.' }
    python -m phase169_r10e2_unpositioned_citation.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R3 focused audit failed.' }
    $afterTracked = @(git -c core.quotepath=false diff --name-only HEAD -- . |
        Where-Object { $_ -ne '' } |
        ForEach-Object { $_.Replace('\', '/') } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R3 cannot inspect post-test tracked files.' }
    $afterTargets = @($afterTracked | Where-Object { $targets -contains $_ })
    $afterOther = @($afterTracked | Where-Object { $targets -notcontains $_ })
    $missingTargets = @($targets | Where-Object { $afterTargets -notcontains $_ })
    $added = @($afterOther | Where-Object { $beforeOther -notcontains $_ })
    $removed = @($beforeOther | Where-Object { $afterOther -notcontains $_ })
    Write-Host ('R10E2R3_TRACKED_AFTER=' + ($afterTracked -join '|'))
    Write-Host ('R10E2R3_EXPECTED_PATCHED=' + ($afterTargets -join '|'))
    Write-Host ('R10E2R3_MISSING_PATCHED=' + ($missingTargets -join '|'))
    Write-Host ('R10E2R3_UNRELATED_AFTER=' + ($afterOther -join '|'))
    Write-Host ('R10E2R3_UNRELATED_ADDED=' + ($added -join '|'))
    Write-Host ('R10E2R3_UNRELATED_REMOVED=' + ($removed -join '|'))
    # Preserve the diagnostic even if we have to roll back the six production files.
    $statusReport = [ordered]@{
        phase = '169 R10E2-R3'
        head = $head
        tracked_before = @($beforeTracked)
        tracked_after = @($afterTracked)
        expected_patched = @($afterTargets)
        missing_patched = @($missingTargets)
        before = @($beforeOther)
        after = @($afterOther)
        added = @($added)
        removed = @($removed)
        full_pytest_run = $false
        non_target_files_automatically_reverted = $false
    }
    if (-not (Test-Path $backupFolder)) {
        New-Item -ItemType Directory -Path $backupFolder -Force | Out-Null
    }
    $statusFile = Join-Path $backupFolder 'r10e2r3_tracked_diff.json'
    $statusReport | ConvertTo-Json -Depth 4 |
        Set-Content -LiteralPath $statusFile -Encoding UTF8
    Write-Host ('R10E2R3_TRACKED_DIFF_REPORT=' + $statusFile)
    if ($missingTargets.Count -gt 0) {
        Write-Host 'R10E2R3_INTEGRITY_RESULT=FAIL_MISSING_PATCHED_FILES'
        throw 'R10E2R3 one or more approved patch targets were not changed.'
    }
    if ($added.Count -gt 0 -or $removed.Count -gt 0) {
        Write-Host 'R10E2R3_INTEGRITY_RESULT=FAIL_UNRELATED_TRACKED_CHANGE'
        throw 'R10E2R3 found tracked changes outside the six approved patch targets; see ADDED and REMOVED.'
    }
    Write-Host 'R10E2R3_INTEGRITY_RESULT=PASS'
    $passed = $true
    Write-Host 'R10E2R3_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host ('R10E2R3_PRODUCTION_FILES_CHANGED=' + ($targets -join ','))
    Write-Host 'R10E2R3_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed) {
        foreach ($target in $targets) {
            $backupName = $target.Replace('/', '__') + '.before'
            $old = Join-Path $backupFolder $backupName
            if (-not (Test-Path $old)) { throw "R10E2R3 backup missing: $backupName" }
            [System.IO.File]::WriteAllBytes((Join-Path $root $target), [System.IO.File]::ReadAllBytes($old))
        }
        Write-Host 'R10E2R3_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
