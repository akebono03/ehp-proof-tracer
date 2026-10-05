$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-4 repair2 - test expectation correction"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "[1/5] Confirm production repair is already applied"
$source = Get-Content `
  ".\toda_group_proof_narrative_equation_numbering.py" `
  -Raw

if ($source -notmatch "reference_plans = \[\]") {
  throw "R5-4 production repair was not found. Apply repair1 first."
}

Write-Host "[2/5] Replace only the R5-4 repair test"
Copy-Item `
  "$PackageDir\test_phase158_r5_4_repair_common_equation_numbering.py" `
  ".\tests\test_phase158_r5_4_repair_common_equation_numbering.py" `
  -Force

Write-Host "[3/5] Run focused equation-numbering tests"
python -m pytest -q `
  ".\tests\test_phase158_r5_4_repair_common_equation_numbering.py" `
  ".\tests\test_phase144_5_generic_definition_order_equations.py" `
  ".\tests\test_phase144_5_r2_r2_api.py"

if ($LASTEXITCODE -ne 0) {
  throw "Focused pytest failed with exit code $LASTEXITCODE."
}

Write-Host "[4/5] Re-run R5-4 representative audit"
$AuditRunner = `
  ".\phase158_r5_4_post_unification_numbering_audit_repair1\run_phase158_r5_4.ps1"

if (-not (Test-Path $AuditRunner)) {
  throw "R5-4 audit repair1 package was not found: $AuditRunner"
}

powershell `
  -ExecutionPolicy Bypass `
  -File $AuditRunner

if ($LASTEXITCODE -ne 0) {
  throw "R5-4 audit re-run failed with exit code $LASTEXITCODE."
}

Write-Host "[5/5] Show git diff summary"
git diff --stat -- `
  "toda_group_proof_narrative_equation_numbering.py" `
  "tests/test_phase158_r5_4_repair_common_equation_numbering.py"

Write-Host ""
Write-Host "Phase 158-R5-4 repair2 completed."
Write-Host "Production code was not changed by repair2."
Write-Host "Full pytest is intentionally NOT run."
