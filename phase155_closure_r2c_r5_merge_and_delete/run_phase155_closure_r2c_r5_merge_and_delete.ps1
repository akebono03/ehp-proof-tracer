$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R5 - merge + delete"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "MERGE_CANDIDATE input: 5 -> 2 merged audit-only tests"
Write-Host "DELETE_CANDIDATE:      6 -> deleted"
Write-Host ""
Write-Host "Merged heavy audits will NOT run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/3 Lightweight R2C-R5 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2c_r5_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R5 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply reviewed merge/delete changes"

python `
  "$PackageDir\apply_phase155_closure_r2c_r5.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R5 apply failed."
}

Write-Host ""
Write-Host "3/3 Static deletion/merge verification + lightweight boundary tests"

python `
  "$PackageDir\verify_phase155_closure_r2c_r5.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R5 verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R5 COMPLETE"
Write-Host "=============================================================="
Write-Host "MERGE_CANDIDATE input: 5"
Write-Host "Merged audit-only tests: 2"
Write-Host "DELETE_CANDIDATE deleted: 6"
Write-Host "Audit-only manifest total: 5"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
