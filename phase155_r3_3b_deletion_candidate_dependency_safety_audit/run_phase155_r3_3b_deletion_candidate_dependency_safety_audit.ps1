$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3B - deletion-candidate dependency safety audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$CandidateCsv = Join-Path `
  $RepoRoot `
  "phase155_r3_3a_audit_output\phase155_r3_3a_deletion_candidates.csv"

if (-not (Test-Path $CandidateCsv)) {
  throw "R3-3A deletion-candidate CSV not found: $CandidateCsv"
}

Write-Host "1/2 Focused tests for the R3-3B audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_3b.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3B audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Audit candidate functions, files, helpers, and cross-module imports"
Write-Host "    No existing test is deleted."

python `
  "$PackageDir\audit_phase155_r3_3b.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3B dependency safety audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3B completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_3b_audit_output\phase155_r3_3b_summary.md"
Write-Host "Candidate safety: $RepoRoot\phase155_r3_3b_audit_output\phase155_r3_3b_candidate_safety.csv"
Write-Host "File safety: $RepoRoot\phase155_r3_3b_audit_output\phase155_r3_3b_file_safety.csv"
