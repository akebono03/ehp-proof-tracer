$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditPath = Join-Path $AuditDir "audit_phase144_6_r25_10.py"
$OutputPath = Join-Path $AuditDir "phase144_6_r25_10_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10-R6"
Write-Host "Combined UTF-8 + current argument API audit runner"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Audit Python changes: none"
Write-Host "=============================================================="
Write-Host ""

if (-not (Test-Path $AuditPath)) {
  throw "R25-10 audit script not found: $AuditPath"
}

Write-Host "A. Verifying R5 argument-API repair..."
$source = Get-Content -Raw -Encoding UTF8 $AuditPath
if ($source -match "conclusion_block_id") {
  throw "Obsolete conclusion_block_id reference remains. Apply R25-10-R5 first."
}
if ($source -notmatch "conclusion_block\.role\.value") {
  throw "Expected R5 conclusion_block API reference was not found."
}
Write-Host "R5 argument API repair: PASS"
Write-Host ""

Write-Host "B. Setting UTF-8 and import environment..."
$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

python -c "import sys; print('stdout encoding=' + str(sys.stdout.encoding)); print('Unicode preflight: η₂ ν′ σ‴')"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  throw "UTF-8 preflight failed."
}
Write-Host "UTF-8 preflight: PASS"
Write-Host ""

Write-Host "C. Syntax/import preflight..."
python -m py_compile $AuditPath
if ($LASTEXITCODE -ne 0) {
  throw "Audit syntax preflight failed."
}
python -c "from toda_group_proof_narrative_contribution_ordering import build_toda_group_proof_narrative_ordered_contributions; import test_phase144_6_r5_18_production_generic_proof_chain_foundation; import audit_phase144_6_r5_22; print('imports: PASS')"
if ($LASTEXITCODE -ne 0) {
  throw "Audit import preflight failed."
}
Write-Host ""

Write-Host "D. Running R25-10 ownership audit..."
if (Test-Path $OutputPath) {
  Remove-Item $OutputPath -Force
}

$Command = 'python -X faulthandler "' + $AuditPath + '" > "' + $OutputPath + '" 2>&1'
cmd /d /c $Command
$AuditExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "---------------- audit output ----------------"
if (Test-Path $OutputPath) {
  Get-Content -Encoding UTF8 $OutputPath
}
Write-Host "-------------- end audit output --------------"
Write-Host ""

Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue

if ($AuditExitCode -ne 0) {
  throw "R25-10 ownership audit failed with exit code $AuditExitCode. See $OutputPath"
}

Write-Host "=============================================================="
Write-Host "R25-10-R6 RESULT: PASS"
Write-Host "Ownership audit completed through Sections A-G."
Write-Host "Production changes: none."
Write-Host "Existing test changes: none."
Write-Host "Audit Python changes: none."
Write-Host "Full suite intentionally not run."
Write-Host "Audit output: $OutputPath"
Write-Host "=============================================================="
