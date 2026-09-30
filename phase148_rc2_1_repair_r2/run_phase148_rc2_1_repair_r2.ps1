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
Write-Host "Phase 148 RC2-1 Repair R2"
Write-Host "Audit harness identity/equality correction"
Write-Host "Production changes: none"
Write-Host "Existing repository test changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepairR1Dir = Join-Path $Root "phase148_rc2_1_repair_r1"
$OriginalAuditDir = Join-Path `
  $Root `
  "phase148_rc2_1_recursive_exactness_exposure_audit"

if (-not (Test-Path $RepairR1Dir)) {
  throw "RC2-1 Repair R1 directory not found: $RepairR1Dir"
}

if (-not (Test-Path $OriginalAuditDir)) {
  throw "Original RC2-1 audit directory not found: $OriginalAuditDir"
}

$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying audit-harness-only repair..."
  Invoke-NativeChecked `
    -Command {
      python "$PackageDir\apply_phase148_rc2_1_repair_r2.py"
    } `
    -FailureMessage "Audit harness repair failed"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked `
    -Command {
      python -m py_compile `
        "$RepairR1Dir\test_phase148_rc2_1_repair_r1.py" `
        "$OriginalAuditDir\audit_phase148_rc2_1.py"
    } `
    -FailureMessage "Syntax preflight failed"

  Write-Host ""
  Write-Host "C. Corrected RC2-1 focused boundary tests..."
  Invoke-NativeChecked `
    -Command {
      pytest -q `
        "$RepairR1Dir\test_phase148_rc2_1_repair_r1.py" `
        "tests\test_phase147_rc1_argument_method_ownership.py" `
        "tests\test_phase143_38_exactness_display_contributions.py" `
        "tests\test_phase143_39_exactness_contribution_ownership.py"
    } `
    -FailureMessage "Focused RC2-1 tests failed"

  Write-Host ""
  Write-Host "D. Exposure audit..."
  python "$OriginalAuditDir\audit_phase148_rc2_1.py" |
    Tee-Object -FilePath "$PackageDir\rc2_1_repair_r2_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "Exposure audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-1 Repair R2: PASS"
  Write-Host "No production changes."
  Write-Host "No repository-wide pytest in RC2-1."
  Write-Host "Next boundary: RC2-2 general exposure-rule design."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
