$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PreviousPackage = Join-Path `
  $RepoRoot `
  "phase155_r6_r1_r2_pi16_reference_normalization_repair"
$PreviousRunner = Join-Path `
  $PreviousPackage `
  "run_phase155_r6_r1_r2_pi16_reference_normalization_repair.ps1"
$PreviousToolTest = Join-Path `
  $PreviousPackage `
  "test_phase155_r6_r1_r2_tools.py"

Write-Host "=============================================================="
Write-Host "Phase 155-R6-R1-R2-R1 - Windows path separator repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This repair is VERY LIGHTWEIGHT."
Write-Host "It changes only one tooling test file in the R6-R1-R2 package."
Write-Host "No production code is changed."
Write-Host "No existing repository test is changed by this repair itself."
Write-Host ""

if (-not (Test-Path $PreviousRunner)) {
  throw "Required previous R6-R1-R2 package not found: $PreviousRunner"
}

Write-Host "1/3 Replace package-local tooling test with OS-independent path assertion"

Copy-Item `
  "$PackageDir\test_phase155_r6_r1_r2_tools.py" `
  $PreviousToolTest `
  -Force

Write-Host ""
Write-Host "2/3 Re-run only lightweight R6-R1-R2 tooling tests"

python -m pytest `
  $PreviousToolTest `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "R6-R1-R2 tooling tests still failed."
}

Write-Host ""
Write-Host "3/3 Continue original R6-R1-R2 runner"

powershell -ExecutionPolicy Bypass `
  -File $PreviousRunner

if ($LASTEXITCODE -ne 0) {
  throw "R6-R1-R2 runner failed after Windows path repair."
}

Write-Host ""
Write-Host "Phase 155-R6-R1-R2-R1 completed."
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Canonical regression: NOT run"
