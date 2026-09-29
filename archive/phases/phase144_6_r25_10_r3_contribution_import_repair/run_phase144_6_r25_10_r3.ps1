$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$RepairRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$AuditRoot = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditScript = Join-Path $AuditRoot "audit_phase144_6_r25_10.py"
$Output = Join-Path $AuditRoot "phase144_6_r25_10_output.txt"
$TestsRoot = Join-Path $ProjectRoot "tests"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10-R3"
Write-Host "Contribution-ordering audit import repair"
Write-Host "Production changes: none"
Write-Host "Existing tests changed: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying audit-only import repair..."
powershell -ExecutionPolicy Bypass `
  -File (Join-Path $RepairRoot "apply_phase144_6_r25_10_r3.ps1")

if ($LASTEXITCODE -ne 0) {
  throw "R25-10-R3 repair failed."
}

Write-Host ""
Write-Host "B. Syntax and import preflight..."
python -m py_compile $AuditScript
if ($LASTEXITCODE -ne 0) {
  throw "Repaired audit script does not compile."
}

$env:PYTHONPATH = "$ProjectRoot;$TestsRoot"

python -c "from toda_group_proof_narrative_contribution_ordering import build_toda_group_proof_narrative_ordered_contributions; print('contribution-ordering import: PASS')"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  throw "Contribution-ordering import preflight failed."
}

python -c "import test_phase144_6_r5_18_production_generic_proof_chain_foundation; import audit_phase144_6_r5_22; print('historical helper imports: PASS')"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  throw "Historical helper import preflight failed."
}

Write-Host "Preflight: PASS"

Write-Host ""
Write-Host "C. Running R25-10 ownership audit..."
if (Test-Path $Output) {
  Remove-Item $Output -Force
}

$Command = 'python -X faulthandler "' + $AuditScript + '" > "' + $Output + '" 2>&1'
cmd /d /c $Command
$AuditExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "---------------- audit output ----------------"
if (Test-Path $Output) {
  Get-Content $Output
}
Write-Host "-------------- end audit output --------------"
Write-Host ""

Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

if ($AuditExitCode -ne 0) {
  throw "R25-10 ownership audit failed with exit code $AuditExitCode. See $Output"
}

Write-Host "=============================================================="
Write-Host "R25-10-R3 RESULT: PASS"
Write-Host "Ownership audit completed."
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
Write-Host "Full suite intentionally not run."
Write-Host "Audit output: $Output"
Write-Host "=============================================================="
