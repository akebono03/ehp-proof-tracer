$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
    throw 'R4D requires the develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect Git HEAD.' }
  Write-Host "R4D_GIT_BRANCH=$branch"
  Write-Host "R4D_GIT_HEAD=$head"
  $before = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect initial tracked Git status.' }

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4d_narrative_audit.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py') `
    (Join-Path $root 'phase169_r3z_reference_only_generic_eta\tests\test_r3z_reference_only_generic_eta.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4D scoped pytest failed.' }

  python -m phase169_r4d_pi64_narrative_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4D narrative audit failed.' }

  $after = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect final tracked Git status.' }
  if (($before -join "`n") -ne ($after -join "`n")) {
    Write-Host 'R4D_CHANGED_TRACKED_FILES:'
    git status --short -uno
    throw 'Tracked Git status changed during R4D. No tracked file will be auto-restored.'
  }
  Write-Host 'R4D_TRACKED_STATUS_UNCHANGED=True'
  Write-Host 'R4D_PRODUCTION_MODIFIED=False'
  Write-Host 'R4D_FULL_PYTEST_RUN=False'
  Write-Host "R4D_JSON=$(Join-Path $PSScriptRoot 'output\audit.json')"
} finally {
  Pop-Location
}
