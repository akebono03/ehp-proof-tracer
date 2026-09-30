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
Write-Host "Phase 148 RC2-1 Repair R1"
Write-Host "Correct audit assumptions and enforce native-command failure"
Write-Host "Production changes: none"
Write-Host "Existing repository test changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OriginalPackageDir = Join-Path `
  $Root `
  "phase148_rc2_1_recursive_exactness_exposure_audit"

if (-not (Test-Path $OriginalPackageDir)) {
  throw "Original RC2-1 package directory not found: $OriginalPackageDir"
}

$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  Invoke-NativeChecked `
    -Command {
      python -m py_compile `
        "$OriginalPackageDir\audit_phase148_rc2_1.py" `
        "$PackageDir\test_phase148_rc2_1_repair_r1.py"
    } `
    -FailureMessage "Syntax preflight failed"

  Write-Host ""
  Write-Host "B. Corrected RC2-1 focused boundary tests..."
  Invoke-NativeChecked `
    -Command {
      pytest -q `
        "$PackageDir\test_phase148_rc2_1_repair_r1.py" `
        "tests\test_phase147_rc1_argument_method_ownership.py" `
        "tests\test_phase143_38_exactness_display_contributions.py" `
        "tests\test_phase143_39_exactness_contribution_ownership.py"
    } `
    -FailureMessage "Focused RC2-1 tests failed"

  Write-Host ""
  Write-Host "C. Re-running exposure audit..."
  python "$OriginalPackageDir\audit_phase148_rc2_1.py" |
    Tee-Object -FilePath "$PackageDir\rc2_1_repair_r1_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "Exposure audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-1 Repair R1: PASS"
  Write-Host "Observed RC2 boundary:"
  Write-Host "  - pi_6^3 owned evidence can form one primary component."
  Write-Host "  - recursive exposure also occurs when an Argument has"
  Write-Host "    exactness evidence but no owned primary component."
  Write-Host "  - RC2-2 must design exposure policy from ownership/relevance,"
  Write-Host "    not from an assumed primary/non-primary split inside pi_6^3."
  Write-Host "No repository-wide pytest in RC2-1."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
