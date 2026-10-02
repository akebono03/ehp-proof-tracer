$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2D - missing execution record audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_2c_r1_audit_output\phase155_r3_2c_r1_root_causes.csv",
  "phase155_r3_2_audit_output\phase155_r3_2_test_executions.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required audit input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R3-2D audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2d.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2D audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Match missing base node IDs against saved execution and fresh collection"
Write-Host "    Only the missing candidate tests are collected with --collect-only."
Write-Host "    No repository-wide pytest is run."

python `
  "$PackageDir\audit_phase155_r3_2d.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2D audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-2D completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2d_audit_output\phase155_r3_2d_summary.md"
Write-Host "Audit rows: $RepoRoot\phase155_r3_2d_audit_output\phase155_r3_2d_missing_execution_audit.csv"
Write-Host "Collection rows: $RepoRoot\phase155_r3_2d_audit_output\phase155_r3_2d_collection_records.csv"
