$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 158-R4-R2 repair2 - equation reference diagnostic"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full pytest: not run"
Write-Host ""

Push-Location $RepoRoot
try {
    Write-Host "[1/3] Confirm current HEAD"
    git rev-parse HEAD
    git log -1 --oneline
    Write-Host ""

    Write-Host "[2/3] Show current public equation reference forms"
    python "$PackageDir\diagnose_phase158_r4_r2_repair2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Diagnostic failed."
    }
    Write-Host ""

    Write-Host "[3/3] Re-run only the remaining failing test"
    pytest -q `
      ".\tests\test_phase158_r4_equation_numbering_and_prose.py::test_phase158_r4_public_equation_tags_are_used_and_compact"
    Write-Host "Focused pytest exit code: $LASTEXITCODE"
    Write-Host ""
    Write-Host "No production or existing test files were modified."
}
finally {
    Pop-Location
}
