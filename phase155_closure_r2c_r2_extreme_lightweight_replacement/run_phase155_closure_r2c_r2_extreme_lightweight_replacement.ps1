$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R2 - extreme lightweight replacement"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Replaces exactly the three known 120s+ tests."
Write-Host "The old 508s / 281s / 276s fixtures will NOT run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/3 Lightweight R2C-R2 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2c_r2_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R2 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply the three reviewed lightweight replacements"

python `
  "$PackageDir\apply_phase155_closure_r2c_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R2 apply failed."
}

Write-Host ""
Write-Host "3/3 Run only the three replacement tests"

python `
  "$PackageDir\verify_phase155_closure_r2c_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R2 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R2 COMPLETE"
Write-Host "=============================================================="
Write-Host "Extreme tests replaced: 3"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
