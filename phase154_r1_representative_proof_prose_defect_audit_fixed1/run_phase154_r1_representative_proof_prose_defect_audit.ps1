$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R1 - Representative Proof Prose Defect Audit"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host ""

Write-Host "Focused baseline tests:"
python -m pytest `
  tests/test_phase144_6_public_route_cutover.py `
  tests/test_phase153_r3_4_reference_statement_rendering_connection.py `
  tests/test_phase153_r3_5_reference_body_duplicate_suppression.py `
  tests/test_phase153_closure_repair_r13.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Focused baseline tests failed."
}

Write-Host ""
Write-Host "Running Phase 154-R1 audit..."
python ".\phase154_r1_representative_proof_prose_defect_audit\audit_phase154_r1_representative_proof_prose_defects.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R1 audit failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R1 audit completed"
Write-Host "=============================================================================="
Write-Host "Please send back:"
Write-Host "  1. the console output"
Write-Host "  2. phase154_r1_representative_proof_prose_defect_audit\phase154_r1_output\phase154_r1_defect_report.md"
