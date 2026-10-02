$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3A - removable duplicate graph audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$VerifiedCsv = Join-Path `
  $RepoRoot `
  "phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv"

if (-not (Test-Path $VerifiedCsv)) {
  throw "R3-2F-r1 verified-pairs CSV not found: $VerifiedCsv"
}

Write-Host "1/2 Focused tests for the R3-3A audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_3a.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3A audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Build removable graph and canonical survivor audit"
Write-Host "    No existing test is deleted."

python `
  "$PackageDir\audit_phase155_r3_3a.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3A graph audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3A completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_3a_audit_output\phase155_r3_3a_summary.md"
Write-Host "Components: $RepoRoot\phase155_r3_3a_audit_output\phase155_r3_3a_components.csv"
Write-Host "Deletion candidates: $RepoRoot\phase155_r3_3a_audit_output\phase155_r3_3a_deletion_candidates.csv"
