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
    throw 'R4B requires the develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD.' }
  Write-Host "R4B_GIT_BRANCH=$branch"
  Write-Host "R4B_GIT_HEAD=$head"

  python -m phase169_r4b_prop44_injectivity.patch
  if ($LASTEXITCODE -ne 0) { throw 'R4B patch failed.' }
  $patchDone = $true

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4b_prop44_injectivity.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py') `
    (Join-Path $root 'phase169_r4a1_prop44_audit_import_fix\tests\test_r4a.py') `
    (Join-Path $root 'phase169_r4a1_prop44_audit_import_fix\tests\test_r4a1_runner.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4B focused pytest failed.' }

  python -m phase169_r4b_prop44_injectivity.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4B proof audit failed.' }

  $changed = @(git diff --name-only)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect git diff.' }
  $notAllowed = @($changed | Where-Object { $_ -ne 'phase165_r52_r9_shared_math.py' })
  if ($notAllowed.Count -gt 0) {
    throw ('R4B changed unrelated tracked files: ' + ($notAllowed -join ', '))
  }
  $success = $true
  Write-Host 'R4B_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py'
  Write-Host 'R4B_FULL_PYTEST_RUN=False'
  Write-Host "R4B_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patchDone -and -not $success -and (Test-Path $backup)) {
    [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
    Write-Host 'R4B_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}
