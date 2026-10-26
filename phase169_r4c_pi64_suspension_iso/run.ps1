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
    throw 'R4C requires develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD.' }
  Write-Host "R4C_GIT_BRANCH=$branch"
  Write-Host "R4C1_GIT_HEAD=$head"

  python -m phase169_r4c_pi64_suspension_iso.patch
  if ($LASTEXITCODE -ne 0) { throw 'R4C1 patch failed.' }
  $patchDone = $true

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4c_pi64_suspension_iso.py') `
    (Join-Path $PSScriptRoot 'tests\test_r4c1_patch_baseline.py') `
    (Join-Path $root 'phase169_r4b_prop44_injectivity\tests\test_r4b_prop44_injectivity.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4C1 focused pytest failed.' }

  python -m phase169_r4c_pi64_suspension_iso.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4C1 cited isomorphism audit failed.' }

  $changed = @(git diff --name-only)
  if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect tracked changes.' }
  $extra = @($changed | Where-Object { $_ -ne 'phase165_r52_r9_shared_math.py' })
  if ($extra.Count -gt 0) {
    throw ('R4C introduced or inherited other tracked edits: ' + ($extra -join ', '))
  }
  $success = $true
  Write-Host 'R4C1_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py'
  Write-Host 'R4C1_FULL_PYTEST_RUN=False'
  Write-Host "R4C1_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patchDone -and -not $success -and (Test-Path $backup)) {
    [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
    Write-Host 'R4C1_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}
