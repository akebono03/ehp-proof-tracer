$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 158-R4-R2 repair3 - final public equation contract"
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

    Write-Host "[2/5] Apply repair3"
    python "$PackageDir\apply_phase158_r4_r2_repair3.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Apply repair3 failed."
    }
    Write-Host ""

    Write-Host "[3/5] Run focused R4 tests"
    pytest -q `
      ".\tests\test_phase144_5_generic_definition_order_equations.py" `
      ".\tests\test_phase157_r20_repair47_injective_image_order_reason.py" `
      ".\tests\test_phase150_rc4_7d_generic_reason_vocabulary.py::test_phase150_rc4_7d_pi16_order_and_final_reasons" `
      ".\tests\test_phase150_rc4_7d_3_public_narrative_generic_route.py::test_phase150_rc4_7d_3_pi16_public_and_web_use_generic_reason_route" `
      ".\tests\test_phase158_r4_equation_numbering_and_prose.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused R4 tests failed."
    }
    Write-Host ""

    Write-Host "[4/5] Run 112-group public re-audit"
    python "$PackageDir\audit_phase158_r4_r2_repair3.py"
    if ($LASTEXITCODE -ne 0) {
        throw "112-group public re-audit found remaining defects."
    }
    Write-Host ""

    Write-Host "[5/5] Show changed files"
    git status --short
    Write-Host ""
    Write-Host "Phase 158-R4-R2 repair3 verification complete."
    Write-Host "Full pytest was intentionally not run."
}
finally {
    Pop-Location
}
