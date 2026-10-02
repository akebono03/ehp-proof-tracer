$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2E - parameterized failure decomposition"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$AuditCsv = Join-Path `
  $RepoRoot `
  "phase155_r3_2d_audit_output\phase155_r3_2d_missing_execution_audit.csv"

if (-not (Test-Path $AuditCsv)) {
  throw "R3-2D audit CSV not found: $AuditCsv"
}

Write-Host "1/2 Focused tests for the R3-2E audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2e.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2E audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Fresh focused execution of unique missing base tests"
Write-Host "    pytest call-phase reports are captured directly."
Write-Host "    This is NOT the repository-wide test suite."

python `
  "$PackageDir\audit_phase155_r3_2e.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2E decomposition failed."
}

Write-Host ""
Write-Host "Phase 155-R3-2E completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2e_audit_output\phase155_r3_2e_summary.md"
Write-Host "Base decomposition: $RepoRoot\phase155_r3_2e_audit_output\phase155_r3_2e_base_decomposition.csv"
Write-Host "Instance reports: $RepoRoot\phase155_r3_2e_audit_output\phase155_r3_2e_instance_reports.csv"
