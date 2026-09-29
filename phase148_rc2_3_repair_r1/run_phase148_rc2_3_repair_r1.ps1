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
Write-Host "Phase 148 RC2-3 Repair R1"
Write-Host "Close direct-premise relocation exposure bypass"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal repair..."
  Invoke-NativeChecked -Command {
    python "$PackageDir\apply_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "RC2-3 Repair R1 apply failed"

  Write-Host ""
  Write-Host "B. Installing focused repair test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_3_repair_r1.py" `
    ".\tests\test_phase148_rc2_3_repair_r1.py" `
    -Force

  Write-Host ""
  Write-Host "C. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "toda_group_proof_narrative_argument_body_renderer.py" `
      "tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "Syntax preflight failed"

  Write-Host ""
  Write-Host "D. RC2-3 Repair R1 focused tests..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_3_repair_r1.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase147_rc1_argument_method_ownership.py" `
      "tests\test_phase143_38_exactness_display_contributions.py" `
      "tests\test_phase143_39_exactness_contribution_ownership.py"
  } -FailureMessage "RC2-3 Repair R1 focused tests failed"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-3 Repair R1: PASS"
  Write-Host "No repository-wide pytest."
  Write-Host "Next boundary after acceptance: RC2-4 cross-group audit."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
