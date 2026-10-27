$ErrorActionPreference = 'Stop'
$scriptDir = $PSScriptRoot
$root = (Resolve-Path (Join-Path $scriptDir '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$backup = Join-Path $scriptDir 'output\phase165_r52_r9_shared_math.py.before'
$patchDone = $false
$success = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS

Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R7 must run on develop.'
    }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot obtain local HEAD.' }
    Write-Host "R7_BRANCH=$branch"
    Write-Host "R7_LOCAL_HEAD=$head"
    $remote = @(git ls-remote origin refs/heads/develop 2>$null)
    if ($LASTEXITCODE -eq 0 -and $remote.Count -gt 0) {
        Write-Host "R7_REMOTE_DEVELOP=$($remote[0].Split("`t")[0])"
    } else {
        Write-Host 'R7_REMOTE_CHECK=UNAVAILABLE'
    }
    $trackedBefore = @(git diff --name-only)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read tracked working-tree changes.' }
    $otherBefore = @($trackedBefore | Where-Object { $_ -ne 'phase165_r52_r9_shared_math.py' } | Sort-Object)

    # Audit-only preflight, before touching production code.
    python -m phase169_r7_general_stable_transport.preflight
    if ($LASTEXITCODE -ne 0) { throw 'R7 preflight failed: production unchanged.' }

    python -m phase169_r7_general_stable_transport.patch
    if ($LASTEXITCODE -ne 0) { throw 'R7 provider patch failed.' }
    $patchDone = $true

    python -m pytest -q `
      (Join-Path $scriptDir 'tests\test_r7_general_stable_transport.py') `
      (Join-Path $root 'phase169_r5b_pi75_prior_transport\tests\test_r5b_pi75_transport.py') `
      (Join-Path $root 'phase169_r6a_pi86_two_step_transport\tests\test_r6a_two_step_transport.py') `
      (Join-Path $root 'phase169_r3m_prior_result_catalog\tests\test_prior_results.py') `
      (Join-Path $root 'phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py')
    if ($LASTEXITCODE -ne 0) { throw 'R7 focused pytest failed.' }

    python -m phase169_r7_general_stable_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R7 canonical proof and Web audit failed.' }

    $trackedAfter = @(git diff --name-only)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot check final tracked working-tree changes.' }
    $otherAfter = @($trackedAfter | Where-Object { $_ -ne 'phase165_r52_r9_shared_math.py' } | Sort-Object)
    if (($otherBefore -join "`n") -ne ($otherAfter -join "`n")) {
        throw 'An unrelated tracked path changed during R7.'
    }
    $success = $true
    Write-Host 'R7_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R7_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py'
    Write-Host 'R7_FULL_PYTEST_RUN=False'
} finally {
    if ($patchDone -and -not $success -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R7_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
