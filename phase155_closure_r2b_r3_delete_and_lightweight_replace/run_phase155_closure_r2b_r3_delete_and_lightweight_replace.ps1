$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R3 - delete + lightweight replacement"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is FOCUSED."
Write-Host "Repository-wide pytest will NOT run."
Write-Host "Historical heavy audits will NOT run."
Write-Host ""
Write-Host "Changes:"
Write-Host "  delete 8 reviewed obsolete/covered test functions"
Write-Host "  replace 1 heavy cross-group invariant with one-group proof-graph test"
Write-Host "  remove the reviewed 9 nodeids from audit-only manifest"
Write-Host ""

Write-Host "1/3 Lightweight R2B-R3 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2b_r3_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R3 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply reviewed deletions and lightweight replacement"

python `
  "$PackageDir\apply_phase155_closure_r2b_r3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R3 repository update failed."
}

Write-Host ""
Write-Host "3/3 Static verification + one lightweight focused test"

python `
  "$PackageDir\verify_phase155_closure_r2b_r3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R3 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R3 COMPLETE"
Write-Host "=============================================================="
Write-Host "Deleted historical test functions: 8"
Write-Host "Lightweight replacement: 1"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
