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
Write-Host "Phase 148 RC2-4 Repair R4.2-R1"
Write-Host "Web depth assertion repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying test-only assertion repair..."
  Invoke-NativeChecked -Command {
    python "$PackageDir\apply_phase148_rc2_4_repair_r4_2_r1.py"
  } -FailureMessage "R4.2-R1 assertion repair failed"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "toda_group_proof_narrative_semantics.py" `
      "tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
      "tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
      ".\phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure\audit_phase148_rc2_4_repair_r4_2.py"
  } -FailureMessage "R4.2-R1 syntax preflight failed"

  Write-Host ""
  Write-Host "C. Re-running R4.2 focused regression..."
  Invoke-NativeChecked -Command {
    pytest -q `
      "tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
      "tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py" `
      "tests\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py" `
      "tests\test_phase148_rc2_4_repair_r4_1_r1.py" `
      "tests\test_phase144_5_generic_definition_order_equations.py" `
      "tests\test_phase143_61b_direct_premise_narrative.py" `
      "tests\test_phase148_rc2_4_repair_r2.py" `
      "tests\test_phase148_rc2_4_repair_r1_exposure_path_audit.py" `
      "tests\test_phase148_rc2_3_exactness_exposure.py" `
      "tests\test_phase148_rc2_3_repair_r1.py" `
      "tests\test_phase118_4_depth_browser_usability.py"
  } -FailureMessage "R4.2-R1 focused regression failed"

  Write-Host ""
  Write-Host "D. Running R4.2 post-repair audit..."
  & python `
    ".\phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure\audit_phase148_rc2_4_repair_r4_2.py" |
    Tee-Object `
      -FilePath "$PackageDir\rc2_4_repair_r4_2_r1_output.txt"

  if ($LASTEXITCODE -ne 0) {
    throw "R4.2-R1 post-repair audit failed (exit code $LASTEXITCODE)"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-4 Repair R4.2-R1: PASS"
  Write-Host "Production changes in R4.2-R1: none."
  Write-Host "Repository-wide pytest: not run."
  Write-Host "Next: six-group RC2-4 post-repair cross-group audit."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
