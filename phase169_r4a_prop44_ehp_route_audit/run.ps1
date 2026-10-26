$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
    throw 'Phase 169 R4A requires the develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD.' }
  Write-Host "R4A_GIT_BRANCH=$branch"
  Write-Host "R4A_GIT_HEAD=$head"
  $before = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read tracked Git status.' }
  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4a.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4A focused pytest failed.' }
  python (Join-Path $PSScriptRoot 'audit.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4A audit failed.' }
  $after = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot re-read tracked Git status.' }
  if (($before -join "`n") -ne ($after -join "`n")) {
    throw 'Tracked Git status changed during R4A audit.'
  }
  Write-Host 'R4A_TRACKED_STATUS_UNCHANGED=True'
  Write-Host 'R4A_FULL_PYTEST_RUN=False'
  Write-Host 'R4A_AUDIT_ONLY=True'
} finally {
  Pop-Location
}
