$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154 - Punctuation Closure Audit Repair1"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Repair:"
Write-Host "  add repository root to Python sys.path before project imports"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Write-Host "Focused R6 baseline tests:"
python -m pytest `
  tests/test_phase154_r6_2_ascii_comma_normalization.py `
  tests/test_phase154_r6_2_repair1_missing_shared_sources.py `
  tests/test_phase154_r6_2_repair2_equation_numbering.py `
  tests/test_phase154_r6_1_repair3_ascii_period_policy.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154 punctuation closure baseline tests failed."
}

Write-Host ""
Write-Host "All-group punctuation closure audit:"
python ".\phase154_punctuation_closure_audit_repair1_import_path\audit_phase154_punctuation_closure.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154 punctuation closure audit found unresolved findings."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154 punctuation closure audit Repair1 completed"
Write-Host "=============================================================================="
Write-Host "Production changes: none"
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
