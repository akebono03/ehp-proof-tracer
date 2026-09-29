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
Write-Host "Phase 148 RC2-4 Repair R1 Exposure-path Audit"
Write-Host "Production changes: none"
Write-Host "Existing repository test changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Installing audit-only test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
    ".\tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4_repair_r1.py" `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py"
  } -FailureMessage "RC2-4 Repair R1 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Audit-harness focused tests..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "RC2-4 Repair R1 focused tests failed"

  Write-Host ""
  Write-Host "D. pi_6^3 exposure-path reverse trace..."
  & python "$PackageDir\audit_phase148_rc2_4_repair_r1.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r1_exposure_path_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "RC2-4 Repair R1 diagnostic audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC2-4 Repair R1 audit completed."
  Write-Host "Production changes: none."
  Write-Host "No repository-wide pytest."
  Write-Host "Use the reverse trace to choose the minimal RC2 repair."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
