$ErrorActionPreference = "Stop"

function Invoke-NativeChecked {
  param(
    [Parameter(Mandatory=$true)]
    [scriptblock]$Command,
    [Parameter(Mandatory=$true)]
    [string]$FailureMessage
  )
  & $Command
  if ($LASTEXITCODE -ne 0) {
    throw "$FailureMessage (exit code $LASTEXITCODE)"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-4 Repair R3"
Write-Host "Web / unit rendering-path parity audit"
Write-Host "Production changes: none"
Write-Host "Existing production tests changed: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Installing audit-only test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py" `
    ".\tests\test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4_repair_r3.py" `
      "tests\test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py"
  } -FailureMessage "R3 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Focused audit tests..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py" `
      "tests\test_phase148_rc2_4_repair_r2.py" `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "R3 focused audit tests failed"

  Write-Host ""
  Write-Host "D. Running Web / unit parity audit..."
  & python "$PackageDir\audit_phase148_rc2_4_repair_r3.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r3_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R3 audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R3 audit completed."
  Write-Host "Production changes: none."
  Write-Host "No repository-wide pytest."
  Write-Host "Use the parity output to select the next minimal repair."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
