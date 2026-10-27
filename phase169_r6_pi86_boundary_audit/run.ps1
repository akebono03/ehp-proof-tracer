$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R6 requires develop branch.' }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect Git HEAD.' }
  $before = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect tracked Git state.' }
  Write-Host "R6_GIT_BRANCH=$branch"
  Write-Host "R6_GIT_HEAD=$head"

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r6_pi86_boundary.py') `
    (Join-Path $root 'phase169_r5b_pi75_prior_transport\tests\test_r5b_pi75_transport.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
  if ($LASTEXITCODE -ne 0) { throw 'R6 focused pytest failed.' }

  python -m phase169_r6_pi86_boundary_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R6 read-only audit failed.' }

  $after = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect final tracked Git state.' }
  if ((@($before) -join "`n") -ne (@($after) -join "`n")) {
    Write-Host 'R6_TRACKED_STATUS_UNCHANGED=False'
    git status --short -uno
    throw 'R6 changed tracked Git state.'
  }
  Write-Host 'R6_TRACKED_STATUS_UNCHANGED=True'
  Write-Host 'R6_PRODUCTION_MODIFIED=False'
  Write-Host 'R6_FULL_PYTEST_RUN=False'
} finally {
  Pop-Location
}
