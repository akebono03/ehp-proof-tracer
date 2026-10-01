$ErrorActionPreference = "Stop"

Write-Host "=============================================================================="
Write-Host "Phase 153-R3-1 - 112 Groups Reference Statement Coverage Audit"
Write-Host "=============================================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "Repository root:"
Write-Host "  $RepoRoot"

Write-Host ""
Write-Host "A. Running audit-only script..."
python ".\phase153_r3_1_reference_statement_coverage_audit\audit_phase153_r3_1_reference_statement_coverage.py"

if ($LASTEXITCODE -ne 0) {
    throw "Phase153-R3-1 audit failed."
}

Write-Host ""
Write-Host "B. Production files changed by this package: none"
Write-Host "C. Full pytest: intentionally not run in audit-only R3-1"
Write-Host ""
Write-Host "Audit outputs:"
Write-Host "  .\phase153_r3_1_reference_statement_coverage_audit\audit_output\reference_statement_coverage_summary.txt"
Write-Host "  .\phase153_r3_1_reference_statement_coverage_audit\audit_output\reference_entry_coverage.csv"
Write-Host "  .\phase153_r3_1_reference_statement_coverage_audit\audit_output\reference_statement_candidates.csv"
Write-Host "  .\phase153_r3_1_reference_statement_coverage_audit\audit_output\reference_entry_category_summary.csv"
Write-Host "  .\phase153_r3_1_reference_statement_coverage_audit\audit_output\reference_statement_type_summary.csv"
Write-Host "  .\phase153_r3_1_reference_statement_coverage_audit\audit_output\exception_inventory.csv"
Write-Host ""
Write-Host "PASS: Phase153-R3-1 audit package completed."
