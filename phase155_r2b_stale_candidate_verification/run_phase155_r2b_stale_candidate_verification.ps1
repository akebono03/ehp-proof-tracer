$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R2B - stale candidate verification"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "1/2 Focused tests for the R2B verification tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r2b.py" `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2B audit-tool focused tests failed."
}

Write-Host ""
Write-Host "2/2 Verify only R2 high-candidate test functions"
Write-Host "    This does NOT run the repository-wide test suite."
Write-Host "    Assertion failures are recorded as confirmed-stale evidence;"
Write-Host "    they do not make this audit script fail."

python "$PackageDir\audit_phase155_r2b.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2B verification audit failed to complete."
}

Write-Host ""
Write-Host "Phase 155-R2B completed."
Write-Host "Summary: $RepoRoot\phase155_r2b_audit_output\phase155_r2b_summary.md"
Write-Host "Verified findings: $RepoRoot\phase155_r2b_audit_output\phase155_r2b_verified_findings.csv"
Write-Host "Focused executions: $RepoRoot\phase155_r2b_audit_output\phase155_r2b_test_executions.csv"
Write-Host "File coverage difference: $RepoRoot\phase155_r2b_audit_output\phase155_r2b_file_coverage_difference.csv"
