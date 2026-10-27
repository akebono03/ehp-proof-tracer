$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$backup = Join-Path $PSScriptRoot 'output\phase165_r52_r9_shared_math.py.before'
$patched = $false
$success = $false
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R6A requires develop branch.' }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD.' }
  Write-Host "R6A_GIT_BRANCH=$branch"
  Write-Host "R6A_GIT_HEAD=$head"
  $otherBefore = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py')
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect initial tracked status.' }

  python -m phase169_r6a_pi86_two_step_transport.patch
  if ($LASTEXITCODE -ne 0) { throw 'R6A patch failed.' }
  $patched = $true

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r6a_patch_guard.py') `
    (Join-Path $PSScriptRoot 'tests\test_r6a_two_step_transport.py') `
    (Join-Path $root 'phase169_r6_pi86_boundary_audit\tests\test_r6_pi86_boundary.py') `
    (Join-Path $root 'phase169_r5b_pi75_prior_transport\tests\test_r5b_pi75_transport.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py')
  if ($LASTEXITCODE -ne 0) { throw 'R6A focused pytest failed.' }

  python -m phase169_r6a_pi86_two_step_transport.audit
  if ($LASTEXITCODE -ne 0) { throw 'R6A proof-tree or narrative audit failed.' }

  $otherAfter = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py')
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect final tracked status.' }
  if ((@($otherBefore | Sort-Object) -join "`n") -ne (@($otherAfter | Sort-Object) -join "`n")) {
    throw 'Unrelated tracked files changed during R6A.'
  }
  $modified = @(git diff --name-only -- phase165_r52_r9_shared_math.py)
  if ($LASTEXITCODE -ne 0 -or $modified.Count -ne 1) {
    throw 'Expected exactly one changed production provider file.'
  }
  $success = $true
  Write-Host 'R6A_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py'
  Write-Host 'R6A_FULL_PYTEST_RUN=False'
  Write-Host "R6A_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patched -and -not $success -and (Test-Path $backup)) {
    [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
    Write-Host 'R6A_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}
