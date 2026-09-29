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
Write-Host "Phase 148 RC2-4 Repair R4.1"
Write-Host "Numbered-equation dependency audit"
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
    "$PackageDir\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py" `
    ".\tests\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4_repair_r4_1.py" `
      "tests\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py"
  } -FailureMessage "R4.1 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Focused audit regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py" `
      "tests\test_phase144_5_generic_definition_order_equations.py" `
      "tests\test_phase143_61b_direct_premise_narrative.py" `
      "tests\test_phase148_rc2_4_repair_r2.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py"
  } -FailureMessage "R4.1 focused audit regression failed"

  Write-Host ""
  Write-Host "D. Running dependency audit..."
  & python "$PackageDir\audit_phase148_rc2_4_repair_r4_1.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r4_1_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R4.1 dependency audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R4.1 audit completed."
  Write-Host "Production changes: none."
  Write-Host "No repository-wide pytest."
  Write-Host "Next: choose the minimal R4.2 dependency repair from this audit."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
