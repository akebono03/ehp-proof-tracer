$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R3 - remaining lightweight + audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Changes:"
Write-Host "  remaining LIGHTWEIGHT_REPLACE: 6"
Write-Host "  new AUDIT_ONLY:                 1"
Write-Host ""
Write-Host "The 112-group audit will NOT run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/3 Lightweight R2C-R3 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2c_r3_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R3 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply six replacements and one audit-only boundary"

python `
  "$PackageDir\apply_phase155_closure_r2c_r3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R3 apply failed."
}

Write-Host ""
Write-Host "3/3 Run only six lightweight replacements + boundary tests"

python `
  "$PackageDir\verify_phase155_closure_r2c_r3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R3 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R3 COMPLETE"
Write-Host "=============================================================="
Write-Host "Lightweight replacements: 6"
Write-Host "New audit-only tests: 1"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
