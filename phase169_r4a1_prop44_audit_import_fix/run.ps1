$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
    throw 'Phase 169 R4A1 requires the develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD.' }
  Write-Host "R4A1_GIT_BRANCH=$branch"
  Write-Host "R4A1_GIT_HEAD=$head"
  $before = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read tracked Git status.' }
  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4a.py') `
    (Join-Path $PSScriptRoot 'tests\test_r4a1_runner.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4A1 focused pytest failed.' }
  # Run as a module, with the repository root on sys.path.
  python -m phase169_r4a1_prop44_audit_import_fix.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4A1 audit failed.' }
  $after = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot re-read tracked Git status.' }
  if (($before -join "`n") -ne ($after -join "`n")) {
    throw 'Tracked Git status changed during R4A1 audit.'
  }
  Write-Host 'R4A1_TRACKED_STATUS_UNCHANGED=True'
  Write-Host 'R4A1_FULL_PYTEST_RUN=False'
  Write-Host 'R4A1_AUDIT_ONLY=True'
  Write-Host 'R4A1_PRODUCTION_MODIFIED=False'
  Write-Host "R4A1_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  Pop-Location
}
