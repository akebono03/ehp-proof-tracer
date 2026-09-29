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
Write-Host "Phase 148 RC2-4 Cross-group Audit"
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
    "$PackageDir\test_phase148_rc2_4_cross_group_audit.py" `
    ".\tests\test_phase148_rc2_4_cross_group_audit.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4.py" `
      "tests\test_phase148_rc2_4_cross_group_audit.py"
  } -FailureMessage "RC2-4 syntax preflight failed"

  Write-Host ""
  Write-Host "C. RC2-4 cross-group focused tests..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_cross_group_audit.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase148_rc2_3_repair_r1.py" `
      "tests\test_phase147_rc1_argument_method_ownership.py" `
      "tests\test_phase143_38_exactness_display_contributions.py" `
      "tests\test_phase143_39_exactness_contribution_ownership.py"
  } -FailureMessage "RC2-4 cross-group focused tests failed"

  Write-Host ""
  Write-Host "D. Six-group diagnostic audit..."
  & python "$PackageDir\audit_phase148_rc2_4.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_cross_group_audit_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "RC2-4 diagnostic audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4: PASS"
  Write-Host "Production changes: none."
  Write-Host "No repository-wide pytest in RC2-4."
  Write-Host "Next boundary: RC2-5 Phase 148 final regression."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
