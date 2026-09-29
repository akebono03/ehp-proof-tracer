$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditRoot = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditScript = Join-Path $AuditRoot "audit_phase144_6_r25_10.py"
$Output = Join-Path $AuditRoot "phase144_6_r25_10_output.txt"
$TestsRoot = Join-Path $ProjectRoot "tests"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-10-R4"
Write-Host "UTF-8 audit runner repair"
Write-Host "Production changes: none"
Write-Host "Existing tests changed: none"
Write-Host "Audit Python changes: none"
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

Write-Host ""
Write-Host "B. UTF-8/import preflight..."
$env:PYTHONPATH = "$ProjectRoot;$TestsRoot"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

python -c "import sys; from toda_group_proof_narrative_contribution_ordering import build_toda_group_proof_narrative_ordered_contributions; import test_phase144_6_r5_18_production_generic_proof_chain_foundation; print(sys.stdout.encoding); print('Unicode preflight: η₂ ν′ σ‴'); print('imports: PASS')"
if ($LASTEXITCODE -ne 0) {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  throw "UTF-8/import preflight failed."
}
Write-Host "UTF-8/import preflight: PASS"

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
  Get-Content -Encoding UTF8 $Output
}
Write-Host "-------------- end audit output --------------"
Write-Host ""

Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue

if ($AuditExitCode -ne 0) {
  throw "R25-10 ownership audit failed with exit code $AuditExitCode. See $Output"
}

Write-Host "=============================================================="
Write-Host "R25-10-R4 RESULT: PASS"
Write-Host "Ownership audit completed."
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
Write-Host "Audit Python changes: none."
Write-Host "Full suite intentionally not run."
Write-Host "Audit output: $Output"
Write-Host "=============================================================="
