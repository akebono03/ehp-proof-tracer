$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 158-R4-R2 - equation numbering + prose repair"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Full pytest: not run"
Write-Host ""

Push-Location $RepoRoot
try {
    Write-Host "[1/5] Confirm current HEAD"
    git rev-parse HEAD
    git log -1 --oneline
    Write-Host ""

    Write-Host "[2/5] Apply minimal production/test repair"
    python "$PackageDir\apply_phase158_r4_r2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Apply failed."
    }
    Write-Host ""

    Write-Host "[3/5] Run focused tests"
    pytest -q `
      ".\tests\test_phase144_5_generic_definition_order_equations.py" `
      ".\tests\test_phase157_r20_repair47_injective_image_order_reason.py" `
      ".\tests\test_phase150_rc4_7d_generic_reason_vocabulary.py" `
      ".\tests\test_phase150_rc4_7d_3_public_narrative_generic_route.py" `
      ".\tests\test_phase158_r4_equation_numbering_and_prose.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused tests failed."
    }
    Write-Host ""

    Write-Host "[4/5] Run 112-group R4 re-audit"
    python "$PackageDir\audit_phase158_r4_r2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "112-group R4 re-audit found remaining defects."
    }
    Write-Host ""

    Write-Host "[5/5] Show changed files"
    git status --short
    Write-Host ""
    Write-Host "Phase 158-R4-R2 focused verification complete."
    Write-Host "Full pytest was intentionally not run."
}
finally {
    Pop-Location
}
