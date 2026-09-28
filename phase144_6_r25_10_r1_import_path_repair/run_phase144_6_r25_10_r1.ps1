$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$RepairRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$AuditRoot = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditScript = Join-Path $AuditRoot "audit_phase144_6_r25_10.py"
$Output = Join-Path $AuditRoot "phase144_6_r25_10_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10-R1"
Write-Host "Audit import-path repair"
Write-Host "Production changes: none"
Write-Host "Existing tests changed: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying audit-only repair..."
powershell -ExecutionPolicy Bypass `
  -File (Join-Path $RepairRoot "apply_phase144_6_r25_10_r1.ps1")

if ($LASTEXITCODE -ne 0) {
  throw "R25-10-R1 repair failed."
}

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile $AuditScript
if ($LASTEXITCODE -ne 0) {
  throw "Repaired audit script does not compile."
}
Write-Host "Syntax: PASS"

Write-Host ""
Write-Host "C. File-loader preflight..."
$env:PYTHONPATH = $ProjectRoot

python -c "import importlib.util, pathlib; p=pathlib.Path(r'$AuditScript'); s=importlib.util.spec_from_file_location('_r25_10_preflight',p); m=importlib.util.module_from_spec(s); print('audit script path:', p); print('spec loader:', type(s.loader).__name__)"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  throw "File-loader preflight failed."
}
Write-Host "File-loader preflight: PASS"

Write-Host ""
Write-Host "D. Running repaired R25-10 ownership audit..."
python -X faulthandler $AuditScript 2>&1 |
  Tee-Object -FilePath $Output
$AuditExitCode = $LASTEXITCODE

Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

if ($AuditExitCode -ne 0) {
  throw "Repaired R25-10 ownership audit failed with exit code $AuditExitCode."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "R25-10-R1 RESULT: PASS"
Write-Host "Ownership audit completed."
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
Write-Host "Full suite intentionally not run."
Write-Host "Audit output: $Output"
Write-Host "=============================================================="
