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
Write-Host "Phase 148 RC2-4 Repair R5-R2"
Write-Host "Exactness phrase classification audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$R5Dir = ".\phase148_rc2_4_repair_r5_two_group_exposure_path_audit"
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Installing audit-only classification test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r5_r2.py" `
    ".\tests\test_phase148_rc2_4_repair_r5_r2.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4_repair_r5_r2.py" `
      ".\tests\test_phase148_rc2_4_repair_r5_r2.py"
  } -FailureMessage "R5-R2 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Focused classification regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      ".\tests\test_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_repair_r5_r2.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
      ".\tests\test_phase148_rc2_4_repair_r2.py" `
      ".\tests\test_phase148_rc2_3_exactness_exposure.py" `
      ".\tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "R5-R2 focused classification regression failed"

  Write-Host ""
  Write-Host "D. Running phrase classification diagnostic..."
  & python `
    "$PackageDir\audit_phase148_rc2_4_repair_r5_r2.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r5_r2_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R5-R2 phrase classification audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R5-R2 audit: COMPLETE"
  Write-Host "Production changes: none."
  Write-Host "Repository-wide pytest: not run."
  Write-Host "Next: repair the six-group audit invariant if this confirms"
  Write-Host "the remaining phrase is not a raw exactness ProofStep."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
