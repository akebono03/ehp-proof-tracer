$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

function Invoke-NativeChecked {
  param(
    [Parameter(Mandatory = $true)]
    [scriptblock]$Command,
    [Parameter(Mandatory = $true)]
    [string]$FailureMessage
  )

  & $Command

  if ($LASTEXITCODE -ne 0) {
    throw "$FailureMessage (exit code $LASTEXITCODE)"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair3c"
Write-Host "Minimal production implementation"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Push-Location $RepoRoot
try {
  Write-Host "[1/4] Apply minimal production repair"
  Invoke-NativeChecked `
    -Command {
      python `
        ".\phase159_pi4_3_repair3c_minimal_production_implementation\apply_phase159_pi4_3_repair3c.py"
    } `
    -FailureMessage "repair3c apply failed"

  Write-Host ""
  Write-Host "[2/4] Compile changed production files and focused test"
  Invoke-NativeChecked `
    -Command {
      python -m py_compile `
        ".\toda_group_proof_narrative_contribution_ordering.py" `
        ".\toda_group_proof_generic_narrative_renderer.py" `
        ".\tests\test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py"
    } `
    -FailureMessage "repair3c compile check failed"

  Write-Host ""
  Write-Host "[3/4] Run repair3c focused tests"
  Invoke-NativeChecked `
    -Command {
      python -m pytest -q `
        ".\tests\test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py"
    } `
    -FailureMessage "repair3c focused tests failed"

  Write-Host ""
  Write-Host "[4/4] Run existing contribution-ordering boundary tests"
  Invoke-NativeChecked `
    -Command {
      python -m pytest -q `
        ".\tests\test_phase143_39_exactness_contribution_ownership.py" `
        ".\tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py" `
        ".\tests\test_phase149_rc3_3_minimal_ordering.py"
    } `
    -FailureMessage "repair3c existing focused regression failed"
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3c focused verification complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
