$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R4-2 - canonical boundary validation"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion/move/marker changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r4_1_audit_output\phase155_r4_1_test_classification.csv",
  "tests"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155-R4-1 input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R4-2 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r4_2.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-2 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Validate canonical boundary against current public modules"
Write-Host "    Public-module use is traced through same-file helper calls."
Write-Host "    No test execution beyond collect-only."

python `
  "$PackageDir\audit_phase155_r4_2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-2 canonical boundary validation failed."
}

Write-Host ""
Write-Host "Phase 155-R4-2 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r4_2_audit_output\phase155_r4_2_summary.md"
Write-Host "Proposed classification: $RepoRoot\phase155_r4_2_audit_output\phase155_r4_2_proposed_classification.csv"
Write-Host "Public surface matrix: $RepoRoot\phase155_r4_2_audit_output\phase155_r4_2_public_surface_matrix.json"
Write-Host "Next: Phase 155-R4-3 review-required lineage / current-contract consolidation"
