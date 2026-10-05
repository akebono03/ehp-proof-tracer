$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-4 repair - common equation-numbering rule"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "[1/6] Apply minimal production repair"
python "$PackageDir\apply_phase158_r5_4_repair.py"
if ($LASTEXITCODE -ne 0) {
  throw "Apply step failed with exit code $LASTEXITCODE."
}

Write-Host "[2/6] Install focused repair test"
Copy-Item `
  "$PackageDir\test_phase158_r5_4_repair_common_equation_numbering.py" `
  ".\tests\test_phase158_r5_4_repair_common_equation_numbering.py" `
  -Force

Write-Host "[3/6] Syntax check"
python -m py_compile `
  ".\toda_group_proof_narrative_equation_numbering.py" `
  ".\tests\test_phase158_r5_4_repair_common_equation_numbering.py"
if ($LASTEXITCODE -ne 0) {
  throw "Syntax check failed with exit code $LASTEXITCODE."
}

Write-Host "[4/6] Run equation-numbering focused tests"
python -m pytest -q `
  ".\tests\test_phase158_r5_4_repair_common_equation_numbering.py" `
  ".\tests\test_phase144_5_generic_definition_order_equations.py" `
  ".\tests\test_phase144_5_r2_r2_api.py"
if ($LASTEXITCODE -ne 0) {
  throw "Focused pytest failed with exit code $LASTEXITCODE."
}

Write-Host "[5/6] Re-run R5-4 audit if repair1 package is present"
$AuditRunner = `
  ".\phase158_r5_4_post_unification_numbering_audit_repair1\run_phase158_r5_4.ps1"

if (Test-Path $AuditRunner) {
  powershell `
    -ExecutionPolicy Bypass `
    -File $AuditRunner
  if ($LASTEXITCODE -ne 0) {
    throw "R5-4 audit re-run failed with exit code $LASTEXITCODE."
  }
}
else {
  Write-Host "Audit repair1 package not found; skipping automatic audit re-run."
}

Write-Host "[6/6] Show git diff summary"
git diff --stat -- `
  "toda_group_proof_narrative_equation_numbering.py" `
  "tests/test_phase158_r5_4_repair_common_equation_numbering.py"

Write-Host ""
Write-Host "Phase 158-R5-4 repair focused checks completed."
Write-Host "Full pytest is intentionally NOT run; it remains for Phase 158 closure."
