$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-1 - duplicate / superseded candidate audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Write-Host "1/2 Focused tests for the R3-1 audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_1.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-1 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Static duplicate / superseded candidate audit"

python `
  "$PackageDir\audit_phase155_r3_1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-1 static audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-1 completed."
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_1_audit_output\phase155_r3_1_summary.md"
Write-Host "Candidate pairs: $RepoRoot\phase155_r3_1_audit_output\phase155_r3_1_candidate_pairs.csv"
Write-Host "Test inventory: $RepoRoot\phase155_r3_1_audit_output\phase155_r3_1_test_inventory.csv"
