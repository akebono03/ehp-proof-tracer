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
Write-Host "Phase 148 RC2-4 Repair R2.1"
Write-Host "Stale R1 audit-test repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Replacing stale R1 audit-only test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
    ".\tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
    -Force

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "toda_group_proof_narrative_argument_body_renderer.py" `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
      "tests\test_phase148_rc2_4_repair_r2.py" `
      "$PackageDir\audit_phase148_rc2_4_repair_r2_1.py"
  } -FailureMessage "RC2-4 Repair R2.1 syntax preflight failed"

  Write-Host ""
  Write-Host "C. RC2-4 Repair R2 focused regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_repair_r2.py" `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase148_rc2_3_repair_r1.py" `
      "tests\test_phase147_rc1_argument_method_ownership.py" `
      "tests\test_phase143_38_exactness_display_contributions.py" `
      "tests\test_phase143_39_exactness_contribution_ownership.py"
  } -FailureMessage "RC2-4 Repair R2.1 focused regression failed"

  Write-Host ""
  Write-Host "D. Post-repair verification..."
  & python "$PackageDir\audit_phase148_rc2_4_repair_r2_1.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r2_1_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "RC2-4 Repair R2.1 verification failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R2.1: PASS"
  Write-Host "Production changes in R2.1: none."
  Write-Host "No repository-wide pytest."
  Write-Host "Next: six-group RC2-4 post-repair cross-group audit."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
