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
Write-Host "Phase 148 RC2-2 Minimal General Exposure Rule Design"
Write-Host "Design only"
Write-Host "Production changes: none"
Write-Host "Existing repository test changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  Invoke-NativeChecked `
    -Command {
      python -m py_compile `
        "$PackageDir\audit_phase148_rc2_2.py"
    } `
    -FailureMessage "Syntax preflight failed"

  Write-Host ""
  Write-Host "B. Design-boundary audit..."
  Invoke-NativeChecked `
    -Command {
      python "$PackageDir\audit_phase148_rc2_2.py"
    } `
    -FailureMessage "RC2-2 design audit failed"

  Write-Host ""
  Write-Host "C. Existing ownership/relevance boundary tests..."
  Invoke-NativeChecked `
    -Command {
      pytest -q `
        "tests\test_phase147_rc1_argument_method_ownership.py" `
        "tests\test_phase143_39_exactness_contribution_ownership.py"
    } `
    -FailureMessage "Existing boundary tests failed"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-2: PASS"
  Write-Host "No production changes."
  Write-Host "No repository-wide pytest in RC2-2."
  Write-Host "Next boundary: RC2-3 minimal implementation."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
