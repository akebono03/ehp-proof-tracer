$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R5 requires develop branch' }
  Write-Host "R5_GIT_BRANCH=$branch"
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Unable to read HEAD' }
  Write-Host "R5_GIT_HEAD=$head"

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r5_pi75_baseline.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py')
  if ($LASTEXITCODE -ne 0) { throw 'R5 limited pytest failed' }

  python -m phase169_r5_pi75_baseline_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R5 audit failed' }
  Write-Host 'R5_AUDIT_ONLY=True'
  Write-Host 'R5_FULL_PYTEST_RUN=False'
} finally {
  Pop-Location
}
