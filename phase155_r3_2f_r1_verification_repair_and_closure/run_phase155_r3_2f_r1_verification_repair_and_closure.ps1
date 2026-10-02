$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2F-r1 - verification repair and closure"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing test files changed: 2"
Write-Host "Existing test functions changed: 2"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$CandidateCsv = Join-Path `
  $RepoRoot `
  "phase155_r3_1_audit_output\phase155_r3_1_candidate_pairs.csv"

if (-not (Test-Path $CandidateCsv)) {
  throw "R3-1 candidate-pairs CSV not found: $CandidateCsv"
}

Write-Host "1/4 Focused tests for the R3-2F-r1 closure tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2f_r1.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F-r1 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/4 Replace both stale whole-module substring guards with AST control-flow guards"

python `
  "$PackageDir\apply_phase155_r3_2f_r1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F-r1 test repair failed."
}

Write-Host ""
Write-Host "3/4 Focused regression for the two repaired Phase 143 tests"

python -m pytest `
  "tests/test_phase143_1_generic_proof_order.py::test_phase143_1_generic_order_has_no_pi6_specific_hardcoding" `
  "tests/test_phase143_1b_semantic_proof_order.py::test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F-r1 repaired Phase 143 tests failed."
}

Write-Host ""
Write-Host "4/4 Fresh normalized verification for all R3-1 candidate pairs"
Write-Host "    Current source fingerprints are recomputed after the repairs."
Write-Host "    Parameterized node IDs are aggregated to base test IDs."
Write-Host "    This is NOT the repository-wide test suite."

python `
  "$PackageDir\audit_phase155_r3_2f_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2F-r1 closure condition was not satisfied."
}

Write-Host ""
Write-Host "Phase 155-R3-2F-r1 completed."
Write-Host "Production changes: none"
Write-Host "Existing test files changed: 2"
Write-Host "Existing test functions changed: 2"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_summary.md"
Write-Host "Final pairs: $RepoRoot\phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv"
