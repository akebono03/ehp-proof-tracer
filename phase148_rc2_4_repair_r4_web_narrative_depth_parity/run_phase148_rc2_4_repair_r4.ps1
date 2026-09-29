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
Write-Host "Phase 148 RC2-4 Repair R4"
Write-Host "Web Narrative depth parity repair"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal production repair..."
  Invoke-NativeChecked -Command {
    python "$PackageDir\apply_phase148_rc2_4_repair_r4.py"
  } -FailureMessage "R4 production repair failed"

  Write-Host ""
  Write-Host "B. Installing focused R4 test..."
  Copy-Item `
    "$PackageDir\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
    ".\tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
    -Force

  Write-Host ""
  Write-Host "C. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "web_group_proof.py" `
      "tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
      "$PackageDir\audit_phase148_rc2_4_repair_r4.py"
  } -FailureMessage "R4 syntax preflight failed"

  Write-Host ""
  Write-Host "D. R4 focused regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
      "tests\test_phase145_group_proof_defaults.py" `
      "tests\test_phase132_9_web_group_proof_modes.py" `
      "tests\test_phase135_1_web_narrative_display_math.py" `
      "tests\test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py" `
      "tests\test_phase148_rc2_4_repair_r2.py" `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase148_rc2_3_repair_r1.py"
  } -FailureMessage "R4 focused regression failed"

  Write-Host ""
  Write-Host "E. Post-repair Web verification..."
  & python "$PackageDir\audit_phase148_rc2_4_repair_r4.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r4_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R4 post-repair audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R4: PASS"
  Write-Host "Repository-wide pytest: not run."
  Write-Host "Next: six-group RC2-4 post-repair cross-group audit."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
