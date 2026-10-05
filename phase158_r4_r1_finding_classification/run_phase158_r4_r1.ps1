$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 158-R4-R1 - finding classification"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full pytest: not run"
Write-Host ""

Push-Location $RepoRoot
try {
    Write-Host "[1/4] Confirm current HEAD"
    git rev-parse HEAD
    git log -1 --oneline
    Write-Host ""

    Write-Host "[2/4] Run focused existing equation-numbering tests"
    pytest -q ".\tests\test_phase144_5_generic_definition_order_equations.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused equation-numbering tests failed."
    }
    Write-Host ""

    Write-Host "[3/4] Classify the 11 Phase 158-R4 findings"
    python "$PackageDir\inspect_phase158_r4_findings.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Finding classification failed."
    }
    Write-Host ""

    Write-Host "[4/4] Output locations"
    Write-Host "Summary:"
    Write-Host "  $PackageDir\audit_output\summary.txt"
    Write-Host "CSV:"
    Write-Host "  $PackageDir\audit_output\classified_findings.csv"
}
finally {
    Pop-Location
}
