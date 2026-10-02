$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "WARNING: THIS IS A HEAVY PHASE-FINAL RUN."
Write-Host "Repository-wide pytest will run once."
Write-Host "Progress will be printed every 100 completed tests."
Write-Host "Ordinary test failures will not stop pytest at the first failure."
Write-Host "The full output is saved to phase155_closure_output."
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Phase 156 functionality: NOT implemented"
Write-Host ""

Write-Host "1/4 Lightweight Closure tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155 Closure tooling tests failed."
}

Write-Host ""
Write-Host "2/4 Repository-wide full pytest"
Write-Host "    This is the Phase 155 final full-suite run."

python `
  "$PackageDir\run_phase155_full_regression.py" `
  --repo-root "$RepoRoot" `
  --package-dir "$PackageDir"

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "Full pytest failed."
  Write-Host "Documentation was NOT changed."
  Write-Host "Review:"
  Write-Host "  $RepoRoot\phase155_closure_output\phase155_full_pytest.log"
  throw "Phase 155 Closure full regression failed."
}

Write-Host ""
Write-Host "3/4 Update Phase 155 closure documentation"

python `
  "$PackageDir\phase155_update_documents.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155 documentation update failed."
}

Write-Host ""
Write-Host "4/4 Verify full-document outputs"

python `
  "$PackageDir\verify_phase155_closure_documents.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155 closure document verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure COMPLETE"
Write-Host "=============================================================="
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: PASS"
Write-Host "Phase 156 functionality: NOT implemented"
Write-Host ""
Write-Host "Closure summary:"
Write-Host "  $RepoRoot\phase155_closure_output\phase155_closure_summary.md"
Write-Host ""
Write-Host "Full updated documents:"
Write-Host "  $RepoRoot\phase155_closure_output\full_documents\README.md"
Write-Host "  $RepoRoot\phase155_closure_output\full_documents\docs\design.md"
Write-Host "  $RepoRoot\phase155_closure_output\full_documents\docs\development_log.md"
Write-Host "  $RepoRoot\phase155_closure_output\full_documents\docs\roadmap.md"
Write-Host "  $RepoRoot\phase155_closure_output\full_documents\docs\proof_records.md"
Write-Host ""
Write-Host "Next: Phase 156 - Reference statement relevance / minimal display"
