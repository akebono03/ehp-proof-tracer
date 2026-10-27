$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $statusBefore = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot read tracked Git status.' }

  python -m phase169_r4c2_committed_audit.verify
  if ($LASTEXITCODE -ne 0) { throw 'R4C2 committed source verification failed.' }

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4c2_verifier.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py') `
    (Join-Path $root 'phase169_r4b_prop44_injectivity\tests\test_r4b_prop44_injectivity.py') `
    (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4C2 focused pytest failed.' }

  python -m phase169_r4c_pi64_suspension_iso.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4C2 genuine cited E-isomorphism audit failed.' }

  $sourceReport = Join-Path $root 'phase169_r4c_pi64_suspension_iso\output\audit.md'
  $sourceJson = Join-Path $root 'phase169_r4c_pi64_suspension_iso\output\audit.json'
  if (-not (Test-Path $sourceReport) -or -not (Test-Path $sourceJson)) {
    throw 'R4C audit report files were not created.'
  }
  $outdir = Join-Path $PSScriptRoot 'output'
  [System.IO.Directory]::CreateDirectory($outdir) | Out-Null
  Copy-Item -LiteralPath $sourceReport -Destination (Join-Path $outdir 'audit.md') -Force
  Copy-Item -LiteralPath $sourceJson -Destination (Join-Path $outdir 'audit.json') -Force

  python -m phase169_r4c2_committed_audit.verify
  if ($LASTEXITCODE -ne 0) { throw 'Reviewed files changed after audit.' }
  $statusAfter = @(git status --porcelain -uno)
  if ($LASTEXITCODE -ne 0) { throw 'Cannot re-read tracked Git status.' }
  if (($statusBefore -join "`n") -ne ($statusAfter -join "`n")) {
    throw 'Tracked Git status changed during audit.'
  }
  Write-Host 'R4C2_TRACKED_STATUS_UNCHANGED=True'
  Write-Host 'R4C2_PRODUCTION_MODIFIED=False'
  Write-Host 'R4C2_FULL_PYTEST_RUN=False'
  Write-Host "R4C2_REPORT=$(Join-Path $outdir 'audit.md')"
  Write-Host "R4C2_JSON=$(Join-Path $outdir 'audit.json')"
} finally {
  Pop-Location
}
