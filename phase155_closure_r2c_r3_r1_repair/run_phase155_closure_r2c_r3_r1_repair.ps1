$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R3-R1 - focused repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Repairs:"
Write-Host "  Phase96 local TodaGroupQuery import: 2 functions"
Write-Host "  audit boundary Phase144-only -> Phase144 or Phase153: 1 function"
Write-Host ""
Write-Host "112-group audit will NOT run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/3 Lightweight repair tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2c_r3_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R3-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply three focused repairs"

python `
  "$PackageDir\apply_phase155_closure_r2c_r3_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R3-R1 apply failed."
}

Write-Host ""
Write-Host "3/3 Re-run only R2C-R3 focused verification"

python `
  "$PackageDir\verify_phase155_closure_r2c_r3_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R3-R1 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R3-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Changed test functions: 3"
Write-Host "Audit-only manifest total: 3"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
