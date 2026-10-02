$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2B - candidate verification failure audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$VerifiedPairs = Join-Path `
  $RepoRoot `
  "phase155_r3_2_audit_output\phase155_r3_2_verified_pairs.csv"

if (-not (Test-Path $VerifiedPairs)) {
  throw "R3-2 verified-pairs CSV not found: $VerifiedPairs"
}

Write-Host "1/2 Focused tests for the R3-2B audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2b.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2B audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Audit the two failures and seven needs-review pairs"

python `
  "$PackageDir\audit_phase155_r3_2b.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2B audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-2B completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2b_audit_output\phase155_r3_2b_summary.md"
Write-Host "Failing-test audit: $RepoRoot\phase155_r3_2b_audit_output\phase155_r3_2b_failing_test_audit.csv"
Write-Host "Needs-review audit: $RepoRoot\phase155_r3_2b_audit_output\phase155_r3_2b_needs_review_audit.csv"
