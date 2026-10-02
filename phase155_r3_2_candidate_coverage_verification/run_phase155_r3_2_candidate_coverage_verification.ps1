$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2 - candidate coverage verification"
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
  "phase155_r3_1_audit_output\phase155_r3_1_candidate_pairs.csv"

if (-not (Test-Path $CandidateCsv)) {
  throw "R3-1 candidate-pairs CSV not found: $CandidateCsv"
}

Write-Host "1/2 Focused tests for the R3-2 audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Focused execution and source-backed candidate verification"
Write-Host "    Only tests referenced by the 332 R3-1 candidate pairs are executed."
Write-Host "    This is not the repository-wide test suite."

python `
  "$PackageDir\audit_phase155_r3_2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2 candidate verification failed to complete."
}

Write-Host ""
Write-Host "Phase 155-R3-2 completed."
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2_audit_output\phase155_r3_2_summary.md"
Write-Host "Verified pairs: $RepoRoot\phase155_r3_2_audit_output\phase155_r3_2_verified_pairs.csv"
Write-Host "Source evidence: $RepoRoot\phase155_r3_2_audit_output\phase155_r3_2_source_evidence.csv"
Write-Host "Executions: $RepoRoot\phase155_r3_2_audit_output\phase155_r3_2_test_executions.csv"
