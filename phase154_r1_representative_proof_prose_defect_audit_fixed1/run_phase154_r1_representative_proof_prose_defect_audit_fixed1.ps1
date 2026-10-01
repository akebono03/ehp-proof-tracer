$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R1 - Representative Proof Prose Defect Audit - Fixed1"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Repair: replace superseded Phase 153-R3 baseline tests with current Phase 153 contracts"
Write-Host ""

Write-Host "Focused current-baseline tests:"
python -m pytest `
  tests/test_phase144_6_public_route_cutover.py `
  tests/test_phase153_r7_proof_body_relevance.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  tests/test_phase153_closure_repair_r13.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Focused current-baseline tests failed."
}

Write-Host ""
Write-Host "Running Phase 154-R1 audit..."
python ".\phase154_r1_representative_proof_prose_defect_audit_fixed1\audit_phase154_r1_representative_proof_prose_defects.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R1 audit failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R1 audit completed"
Write-Host "=============================================================================="
Write-Host "Please send back:"
Write-Host "  1. the console output"
Write-Host "  2. phase154_r1_representative_proof_prose_defect_audit_fixed1\phase154_r1_output\phase154_r1_defect_report.md"
