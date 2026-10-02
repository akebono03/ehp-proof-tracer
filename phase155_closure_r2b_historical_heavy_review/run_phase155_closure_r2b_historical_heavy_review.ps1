$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B - HISTORICAL_HEAVY review"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is STATIC and LIGHTWEIGHT."
Write-Host "No repository test body will run."
Write-Host "No production file will change."
Write-Host "No existing test file will change."
Write-Host ""
Write-Host "Inputs:"
Write-Host "  phase155_closure_r2_output\historical_heavy_nodeids.txt"
Write-Host "  phase155_closure_output\phase155_full_pytest.log"
Write-Host ""

Write-Host "1/2 Lightweight R2B tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2b_audit.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B tooling tests failed."
}

Write-Host ""
Write-Host "2/2 Static runtime / redundancy review of the 36 Phase144 failures"

python `
  "$PackageDir\phase155_closure_r2b_audit.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B static review failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B review COMPLETE"
Write-Host "=============================================================="
Write-Host "No heavy test executed."
Write-Host "No deletion performed."
Write-Host "No production or existing-test changes."
Write-Host ""
Write-Host "Report:"
Write-Host "  $RepoRoot\phase155_closure_r2b_output\phase155_closure_r2b_review.md"
Write-Host ""
Write-Host "Next:"
Write-Host "  use the report to build a minimal R2B repair package;"
Write-Host "  prefer audit-only moves, shared cached context, and proven superseded deletion."
