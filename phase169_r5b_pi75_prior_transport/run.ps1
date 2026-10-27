$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$backup = Join-Path $PSScriptRoot 'output\phase165_r52_r9_shared_math.py.before'
$patchDone = $false
$success = $false
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
    throw 'R5B requires the develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD.' }
  Write-Host "R5B_GIT_BRANCH=$branch"
  Write-Host "R5B_GIT_HEAD=$head"
  $beforeTracked = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py')
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read initial tracked changes.' }

  python -m phase169_r5b_pi75_prior_transport.patch
  if ($LASTEXITCODE -ne 0) { throw 'R5B patch failed.' }
  $patchDone = $true

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r5b_patch_guard.py') `
    (Join-Path $PSScriptRoot 'tests\test_r5b_pi75_transport.py') `
    (Join-Path $root 'phase169_r5a_pi75_premise_diagnostic\tests\test_r5a_premise_diagnostic.py') `
    (Join-Path $root 'phase169_r5_pi75_baseline_audit\tests\test_r5_pi75_baseline.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py')
  if ($LASTEXITCODE -ne 0) { throw 'R5B focused pytest failed.' }

  python -m phase169_r5b_pi75_prior_transport.audit
  if ($LASTEXITCODE -ne 0) { throw 'R5B cited proof or Web audit failed.' }

  $afterTracked = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py')
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read final tracked changes.' }
  if ((@($beforeTracked | Sort-Object) -join "`n") -ne (@($afterTracked | Sort-Object) -join "`n")) {
    throw 'Unrelated tracked Git status changed during R5B.'
  }
  $changed = @(git diff --name-only -- phase165_r52_r9_shared_math.py)
  if ($LASTEXITCODE -ne 0 -or $changed.Count -ne 1) {
    throw 'Expected exactly one modified production provider.'
  }
  $success = $true
  Write-Host 'R5B_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py'
  Write-Host 'R5B_FULL_PYTEST_RUN=False'
  Write-Host "R5B_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patchDone -and -not $success -and (Test-Path $backup)) {
    [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
    Write-Host 'R5B_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}
