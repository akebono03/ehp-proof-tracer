$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PackageDir = Join-Path $ProjectRoot "phase144_6_r25_10_r5_argument_api_audit_repair"
$AuditDir = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditPath = Join-Path $AuditDir "audit_phase144_6_r25_10.py"
$OutputPath = Join-Path $AuditDir "phase144_6_r25_10_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10-R5 argument API audit repair"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="
Write-Host ""

Write-Host "A. Applying audit-harness-only repair..."
powershell -ExecutionPolicy Bypass -File (Join-Path $PackageDir "apply_phase144_6_r25_10_r5.ps1")
Write-Host ""

Write-Host "B. Verifying repaired Section F reference..."
$source = Get-Content -Raw -Encoding UTF8 $AuditPath
if ($source -match "conclusion_block_id") {
  throw "Obsolete conclusion_block_id reference remains."
}
if ($source -notmatch "conclusion_block\.role\.value") {
  throw "Expected conclusion_block API reference was not found."
}
Write-Host "Section F argument API preflight: PASS"
Write-Host ""

Write-Host "C. Syntax preflight..."
$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"
python -m py_compile $AuditPath
if ($LASTEXITCODE -ne 0) {
  throw "Audit syntax preflight failed."
}
Write-Host "Audit syntax preflight: PASS"
Write-Host ""

Write-Host "D. Running R25-10 ownership audit through Sections A-G..."
$PreviousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
python -X faulthandler $AuditPath 2>&1 | Tee-Object -FilePath $OutputPath
$AuditExitCode = $LASTEXITCODE
$ErrorActionPreference = $PreviousErrorActionPreference

if ($AuditExitCode -ne 0) {
  throw "R25-10 ownership audit failed with exit code $AuditExitCode. See $OutputPath"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "R25-10-R5 RESULT: PASS"
Write-Host "Audit output: $OutputPath"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full pytest: intentionally not run"
Write-Host "=============================================================="
