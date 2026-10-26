$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R5A requires develop' }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read HEAD' }
  Write-Host "R5A_GIT_BRANCH=$branch"
  Write-Host "R5A_GIT_HEAD=$head"
  $before = [string]((git status --porcelain --untracked-files=no) -join "`n")
  if ($LASTEXITCODE -ne 0) { throw 'Cannot check Git status' }
  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r5a_premise_diagnostic.py') `
    (Join-Path $root 'phase169_r5_pi75_baseline_audit\tests\test_r5_pi75_baseline.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
  if ($LASTEXITCODE -ne 0) { throw 'R5A focused pytest failed' }
  python -m phase169_r5a_pi75_premise_diagnostic.audit
  if ($LASTEXITCODE -ne 0) { throw 'R5A diagnostic failed' }
  $after = [string]((git status --porcelain --untracked-files=no) -join "`n")
  if ($LASTEXITCODE -ne 0 -or $after -ne $before) {
    throw 'R5A tracked Git status changed'
  }
  Write-Host 'R5A_AUDIT_ONLY=True'
  Write-Host 'R5A_FULL_PYTEST_RUN=False'
} finally {
  Pop-Location
}
