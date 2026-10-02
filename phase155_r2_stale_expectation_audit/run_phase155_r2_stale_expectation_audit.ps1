$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$R1Inventory = Join-Path $RepoRoot "phase155_r1_audit_output\phase155_r1_test_inventory.csv"
$OutputDir = Join-Path $RepoRoot "phase155_r2_audit_output"

Write-Host "=============================================================="
Write-Host "Phase 155-R2 - stale expectation audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""

if (-not (Test-Path $R1Inventory)) {
    throw "Phase 155-R1 inventory not found: $R1Inventory"
}

Write-Host "1/2 Focused tests for the R2 audit tool only"
python -m pytest "$PackageDir\test_audit_phase155_r2.py" -q
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "2/2 Static stale-expectation audit (does NOT execute repository-wide tests)"
python "$PackageDir\audit_phase155_r2.py" `
    --repo-root "$RepoRoot" `
    --r1-inventory "$R1Inventory" `
    --output-dir "$OutputDir"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 155-R2 completed."
Write-Host "Summary: $OutputDir\phase155_r2_summary.md"
Write-Host "Findings: $OutputDir\phase155_r2_expectation_findings.csv"
Write-Host "File summary: $OutputDir\phase155_r2_file_summary.csv"
