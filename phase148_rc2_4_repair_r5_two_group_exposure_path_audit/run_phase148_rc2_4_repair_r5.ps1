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
Write-Host "Phase 148 RC2-4 Repair R5"
Write-Host "Two-group exactness exposure-path audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Installing audit-only test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r5.py" `
    ".\tests\test_phase148_rc2_4_repair_r5.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_repair_r5.py"
  } -FailureMessage "R5 audit syntax preflight failed"

  Write-Host ""
  Write-Host "C. Focused audit regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      ".\tests\test_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_post_repair_six_group.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
      ".\tests\test_phase148_rc2_4_repair_r2.py" `
      ".\tests\test_phase148_rc2_3_exactness_exposure.py"
  } -FailureMessage "R5 focused audit regression failed"

  Write-Host ""
  Write-Host "D. Running exactness reverse trace..."
  & python `
    "$PackageDir\audit_phase148_rc2_4_repair_r5.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r5_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R5 exposure-path audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R5 audit completed."
  Write-Host "Production changes: none."
  Write-Host "Repository-wide pytest: not run."
  Write-Host "Next: choose the minimal general suppression repair from this trace."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
