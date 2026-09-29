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
Write-Host "Phase 148 RC2-4 Repair R4.1-R1"
Write-Host "Audit harness current-Argument-API repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying audit-harness-only repair..."
  Invoke-NativeChecked -Command {
    python "$PackageDir\apply_phase148_rc2_4_repair_r4_1_r1.py"
  } -FailureMessage "R4.1-R1 audit harness repair failed"

  Write-Host ""
  Write-Host "B. Installing R4.1-R1 audit-harness test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r4_1_r1.py" `
    ".\tests\test_phase148_rc2_4_repair_r4_1_r1.py" `
    -Force

  Write-Host ""
  Write-Host "C. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      ".\phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit\audit_phase148_rc2_4_repair_r4_1.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_1_r1.py"
  } -FailureMessage "R4.1-R1 syntax preflight failed"

  Write-Host ""
  Write-Host "D. Focused audit-harness regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      ".\tests\test_phase148_rc2_4_repair_r4_1_r1.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py" `
      ".\tests\test_phase144_5_generic_definition_order_equations.py" `
      ".\tests\test_phase143_61b_direct_premise_narrative.py" `
      ".\tests\test_phase148_rc2_4_repair_r2.py" `
      ".\tests\test_phase148_rc2_3_exactness_exposure.py"
  } -FailureMessage "R4.1-R1 focused regression failed"

  Write-Host ""
  Write-Host "E. Re-running numbered-equation dependency audit..."
  & python `
    ".\phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit\audit_phase148_rc2_4_repair_r4_1.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r4_1_r1_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R4.1-R1 dependency audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R4.1-R1 audit completed."
  Write-Host "Production changes: none."
  Write-Host "No repository-wide pytest."
  Write-Host "Next: select the minimal R4.2 dependency repair."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
