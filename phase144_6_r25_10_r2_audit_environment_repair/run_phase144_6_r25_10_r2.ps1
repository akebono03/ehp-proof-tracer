$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditRoot = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditScript = Join-Path $AuditRoot "audit_phase144_6_r25_10.py"
$Output = Join-Path $AuditRoot "phase144_6_r25_10_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10-R2"
Write-Host "Audit execution-environment repair"
Write-Host "Production changes: none"
Write-Host "Existing tests changed: none"
Write-Host "Audit Python changes in R2: none"
Write-Host "=============================================================="

if (-not (Test-Path $AuditScript)) {
  throw "R25-10 audit script not found: $AuditScript"
}

Write-Host ""
Write-Host "A. Syntax preflight..."
python -m py_compile $AuditScript
if ($LASTEXITCODE -ne 0) {
  throw "R25-10 audit script does not compile."
}
Write-Host "Syntax: PASS"

Write-Host ""
Write-Host "B. Import-environment preflight..."

$TestsRoot = Join-Path $ProjectRoot "tests"
$env:PYTHONPATH = "$ProjectRoot;$TestsRoot"

python -c "import test_phase144_6_r5_18_production_generic_proof_chain_foundation; print('bare test-helper import: PASS')"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  throw "Bare test-helper import preflight failed."
}

python -c "import audit_phase144_6_r5_22; print('audit helper dependency import: PASS')"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  throw "Audit helper dependency import preflight failed."
}

Write-Host "Import environment: PASS"

Write-Host ""
Write-Host "C. Running repaired R25-10 ownership audit..."
Write-Host "Output file: $Output"

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
Write-Host "R25-10-R2 RESULT: PASS"
Write-Host "Ownership audit completed."
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
Write-Host "Audit Python changes in R2: none."
Write-Host "Full suite intentionally not run."
Write-Host "Audit output: $Output"
Write-Host "=============================================================="
