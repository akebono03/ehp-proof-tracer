$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R4-R1 - focused repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Repairs:"
Write-Host "  boundary test: 23 -> exact final 2"
Write-Host "  Phase42: remove heavy context construction"
Write-Host "  Phase43-10: semantic contract instead of rendered connector text"
Write-Host ""
Write-Host "Heavy audit-only tests will NOT run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/3 Lightweight repair tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2b_r4_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R4-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply three focused test repairs"

python `
  "$PackageDir\apply_phase155_closure_r2b_r4_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R4-R1 apply failed."
}

Write-Host ""
Write-Host "3/3 Run only repaired focused tests"

python `
  "$PackageDir\verify_phase155_closure_r2b_r4_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R4-R1 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R4-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Changed test functions: 3"
Write-Host "Production changes: none"
Write-Host "Audit-only tests retained: 2"
Write-Host "Repository-wide pytest: NOT run"
