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
Write-Host "Phase 148 RC2-4 Repair R5-R1"
Write-Host "Exposure-path audit runner repair"
Write-Host "Production changes: none"
Write-Host "Existing tests changed: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$R5Dir = ".\phase148_rc2_4_repair_r5_two_group_exposure_path_audit"
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Verifying R5 audit files..."
  if (-not (Test-Path "$R5Dir\audit_phase148_rc2_4_repair_r5.py")) {
    throw "R5 audit script not found. Extract the R5 package first."
  }
  if (-not (Test-Path ".\tests\test_phase148_rc2_4_repair_r5.py")) {
    throw "R5 audit-only test not found. Run/extract the R5 package first."
  }

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$R5Dir\audit_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_repair_r5.py"
  } -FailureMessage "R5-R1 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Running diagnostic-safe focused regression..."
  Write-Host "   Note: the still-failing six-group zero-leak completion test"
  Write-Host "   is intentionally excluded until the exposure path is diagnosed."
  Invoke-NativeChecked -Command {
    pytest -q `
      ".\tests\test_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
      ".\tests\test_phase148_rc2_4_repair_r2.py" `
      ".\tests\test_phase148_rc2_3_exactness_exposure.py" `
      ".\tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "R5-R1 diagnostic-safe focused regression failed"

  Write-Host ""
  Write-Host "D. Running exactness reverse trace..."
  & python `
    "$R5Dir\audit_phase148_rc2_4_repair_r5.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r5_r1_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R5-R1 exposure-path audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R5-R1 audit: COMPLETE"
  Write-Host "Production changes: none."
  Write-Host "Existing tests changed: none."
  Write-Host "Repository-wide pytest: not run."
  Write-Host "Next: classify the common leakage path and make only the"
  Write-Host "minimal general RC2 suppression repair."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
