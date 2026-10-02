$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R4-3 - review-required lineage / current-contract consolidation"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion/move/marker changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r4_2_audit_output\phase155_r4_2_proposed_classification.csv",
  "tests"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155-R4-2 input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R4-3 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r4_3.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-3 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Consolidate review-required tests by current production ownership"
Write-Host "    Same-file helper reachability is included."
Write-Host "    tests.* helper-only cases are retained as lineage-support candidates."
Write-Host "    No test execution beyond collect-only."

python `
  "$PackageDir\audit_phase155_r4_3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-3 current-contract consolidation failed."
}

Write-Host ""
Write-Host "Phase 155-R4-3 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r4_3_audit_output\phase155_r4_3_summary.md"
Write-Host "Classification: $RepoRoot\phase155_r4_3_audit_output\phase155_r4_3_consolidated_classification.csv"
Write-Host "Ownership matrix: $RepoRoot\phase155_r4_3_audit_output\phase155_r4_3_production_ownership_matrix.json"
Write-Host "Next: Phase 155-R4-4 canonical command / residual boundary decision"
