$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = (Get-Location).Path
$SourceTest = Join-Path $PackageRoot "payload\tests\test_phase153_scalar_order_narrative_classification.py"
$TargetTest = Join-Path $RepositoryRoot "tests\test_phase153_scalar_order_narrative_classification.py"

Write-Host "=============================================================="
Write-Host "Phase 153-R1 Fixed12"
Write-Host "Direct ScalarGreaterEqualStatement -> ORDER classifier test"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

if (-not (Test-Path $SourceTest)) {
  throw "Bundled test file not found: $SourceTest"
}

if (-not (Test-Path (Join-Path $RepositoryRoot "tests"))) {
  throw "Repository tests directory not found. Run this script from the repository root."
}

Write-Host "A. Applying corrected Phase153-R1 focused test..."
Copy-Item `
  -Path $SourceTest `
  -Destination $TargetTest `
  -Force

Write-Host "Applied:"
Write-Host "  $TargetTest"
Write-Host ""

Write-Host "B. Running Phase134-9 classifier baseline..."
pytest -q tests/test_phase134_9_group_proof_narrative_classifier.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "C. Running Phase153-R1 focused regression..."
pytest -q tests/test_phase153_scalar_order_narrative_classification.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase153-R1 Fixed12 focused checks passed."
Write-Host "=============================================================="
