$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 158-R4-R1 repair1 - equation numbering diagnostic"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full pytest: not run"
Write-Host ""

Push-Location $RepoRoot
try {
    Write-Host "[1/5] Confirm current HEAD"
    git rev-parse HEAD
    git log -1 --oneline
    Write-Host ""

    Write-Host "[2/5] Run focused equation-numbering tests"
    Write-Host "NOTE: failures are diagnostic here and do not stop the script."
    pytest -q ".\tests\test_phase144_5_generic_definition_order_equations.py"
    $FocusedExit = $LASTEXITCODE
    Write-Host "Focused pytest exit code: $FocusedExit"
    Write-Host ""

    Write-Host "[3/5] Inspect current pi_6^3 numbering / transition identity"
    python "$PackageDir\diagnose_phase158_r4_r1_equation_numbering.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Equation-numbering diagnostic failed."
    }
    Write-Host ""

    Write-Host "[4/5] Classify all 11 initial R4 findings"
    python "$PackageDir\classify_phase158_r4_findings.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Finding classification failed."
    }
    Write-Host ""

    Write-Host "[5/5] Output locations"
    Write-Host "Equation diagnostic:"
    Write-Host "  $PackageDir\audit_output\summary.txt"
    Write-Host "Finding classification:"
    Write-Host "  $PackageDir\audit_output\classification_summary.txt"
    Write-Host "CSV:"
    Write-Host "  $PackageDir\audit_output\classified_findings.csv"
    Write-Host ""
    Write-Host "No production or existing test files were modified."
}
finally {
    Pop-Location
}
