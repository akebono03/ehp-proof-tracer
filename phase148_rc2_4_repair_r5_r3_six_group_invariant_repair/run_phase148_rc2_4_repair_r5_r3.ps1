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
Write-Host "Phase 148 RC2-4 Repair R5-R3"
Write-Host "Six-group raw-exactness invariant repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying audit-test-only invariant repair..."
  Invoke-NativeChecked -Command {
    python `
      "$PackageDir\apply_phase148_rc2_4_repair_r5_r3.py"
  } -FailureMessage "R5-R3 audit-test repair failed"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\audit_phase148_rc2_4_repair_r5_r3.py" `
      ".\tests\test_phase148_rc2_4_post_repair_six_group.py"
  } -FailureMessage "R5-R3 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Re-running six-group post-repair regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      ".\tests\test_phase148_rc2_4_post_repair_six_group.py" `
      ".\tests\test_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_repair_r5_r2.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
      ".\tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
      ".\tests\test_phase148_rc2_4_repair_r2.py" `
      ".\tests\test_phase148_rc2_3_exactness_exposure.py" `
      ".\tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "R5-R3 six-group regression failed"

  Write-Host ""
  Write-Host "D. Running corrected six-group diagnostic..."
  & python `
    "$PackageDir\audit_phase148_rc2_4_repair_r5_r3.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r5_r3_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R5-R3 six-group diagnostic failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R5-R3: PASS"
  Write-Host "Production changes: none."
  Write-Host "Repository-wide pytest: not run."
  Write-Host "If all four audit invariants above are True, RC2-4 is complete."
  Write-Host "Next: RC2-5 final regression and documentation closure."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
