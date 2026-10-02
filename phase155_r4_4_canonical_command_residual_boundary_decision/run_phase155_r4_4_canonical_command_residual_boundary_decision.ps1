$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R4-4 - canonical command / residual boundary decision"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "IMPORTANT: collect-only validation may be moderately heavy."
Write-Host "It covers the large canonical candidate set, but DOES NOT execute tests."
Write-Host "Progress will be printed batch by batch."
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r4_3_audit_output\phase155_r4_3_consolidated_classification.csv",
  "phase155_r4_3_audit_output\phase155_r4_3_production_ownership_matrix.json",
  "tests"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155-R4-3 input not found: $FullPath"
  }
}

Write-Host "1/3 Focused tests for the R4-4 build/verification tools"

python -m pytest `
  "$PackageDir\test_phase155_r4_4_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-4 tool tests failed."
}

Write-Host ""
Write-Host "2/3 Build canonical manifest, residual boundary, and reusable runner"

python `
  "$PackageDir\build_phase155_r4_4.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-4 artifact build failed."
}

Write-Host ""
Write-Host "3/3 Validate exact canonical command with collect-only"
Write-Host "    This step may take a while."
Write-Host "    It will print collect batch N/M progress."
Write-Host "    Test bodies are NOT executed."

python `
  "$PackageDir\verify_phase155_r4_4.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-4 canonical boundary verification failed."
}

Write-Host ""
Write-Host "Phase 155-R4-4 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r4_4_audit_output\phase155_r4_4_summary.md"
Write-Host "Verification: $RepoRoot\phase155_r4_4_audit_output\phase155_r4_4_verification_summary.md"
Write-Host ""
Write-Host "Canonical regression command (HEAVY; do NOT run yet for R4):"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\phase155_r4_4_audit_output\run_phase155_canonical_regression.ps1"
Write-Host ""
Write-Host "Next: Phase 155-R5 heavy / historical boundary"
