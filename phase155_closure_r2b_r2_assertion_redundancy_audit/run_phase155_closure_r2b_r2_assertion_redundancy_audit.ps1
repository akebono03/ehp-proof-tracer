$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R2 - assertion-level redundancy audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is STATIC and LIGHTWEIGHT."
Write-Host "No Phase144 heavy test body will run."
Write-Host "No repository file will be deleted or modified."
Write-Host ""

Write-Host "1/2 Lightweight R2B-R2 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2b_r2_audit.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R2 tooling tests failed."
}

Write-Host ""
Write-Host "2/2 Audit the 9 SUPERSEDED_CANDIDATE functions"

python `
  "$PackageDir\phase155_closure_r2b_r2_audit.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R2 assertion-level audit failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R2 COMPLETE"
Write-Host "=============================================================="
Write-Host "Repository tests executed: 0"
Write-Host "Repository files changed: 0"
Write-Host "Deletions performed: 0"
Write-Host ""
Write-Host "Report:"
Write-Host "  $RepoRoot\phase155_closure_r2b_r2_output\phase155_closure_r2b_r2_audit.md"
