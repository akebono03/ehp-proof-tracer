$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")
$OutputDir = Join-Path $RepoRoot "phase155_r1_audit_output"

Write-Host "=============================================================="
Write-Host "Phase 155-R1 — Test inventory / classification audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "1/2 Focused tests for the R1 audit tool only"
python -m pytest (Join-Path $PackageDir "test_audit_phase155_r1.py") -q
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "2/2 Static inventory (does NOT execute repository-wide tests)"
python (Join-Path $PackageDir "audit_phase155_r1.py") `
    --repo-root $RepoRoot `
    --output-dir $OutputDir
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 155-R1 completed."
Write-Host "Summary: $OutputDir\phase155_r1_summary.md"
Write-Host "Inventory: $OutputDir\phase155_r1_test_inventory.csv"
Write-Host "Duplicates: $OutputDir\phase155_r1_duplicate_groups.csv"
