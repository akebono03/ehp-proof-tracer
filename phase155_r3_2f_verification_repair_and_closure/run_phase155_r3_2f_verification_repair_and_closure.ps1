$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2F - verification repair and closure"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing test files changed: 2"
Write-Host "Existing test functions changed: 2"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_1_audit_output\phase155_r3_1_candidate_pairs.csv",
  "phase155_r3_2_audit_output\phase155_r3_2_verified_pairs.csv",
  "phase155_r3_2_audit_output\phase155_r3_2_source_evidence.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required R3 audit input not found: $FullPath"
  }
}

Write-Host "1/4 Focused tests for the R3-2F closure audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2f.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F audit-tool tests failed."
}

Write-Host ""
Write-Host "2/4 Apply the two stale Phase 143 expectation repairs"

python `
  "$PackageDir\apply_phase155_r3_2f.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F test repair failed."
}

Write-Host ""
Write-Host "3/4 Focused regression for the two repaired test functions"

python -m pytest `
  "tests/test_phase143_1_generic_proof_order.py::test_phase143_1_generic_order_has_no_pi6_specific_hardcoding" `
  "tests/test_phase143_1b_semantic_proof_order.py::test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F repaired Phase 143 tests failed."
}

Write-Host ""
Write-Host "4/4 Re-run normalized candidate verification for all R3-1 pairs"
Write-Host "    Parameterized pytest node IDs are aggregated to base test IDs."
Write-Host "    This is NOT the repository-wide test suite."

python `
  "$PackageDir\audit_phase155_r3_2f.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F closure condition was not satisfied."
}

Write-Host ""
Write-Host "Phase 155-R3-2F completed."
Write-Host "Production changes: none"
Write-Host "Existing test files changed: 2"
Write-Host "Existing test functions changed: 2"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2f_audit_output\phase155_r3_2f_summary.md"
Write-Host "Final pairs: $RepoRoot\phase155_r3_2f_audit_output\phase155_r3_2f_verified_pairs.csv"
