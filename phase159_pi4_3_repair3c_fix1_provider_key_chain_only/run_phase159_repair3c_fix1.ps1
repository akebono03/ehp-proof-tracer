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
Write-Host "Phase 159 - repair3c fix1"
Write-Host "Provider-key chain-only optimization"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Push-Location $RepoRoot
try {
  Write-Host "[1/5] Apply minimal production fix"
  Invoke-NativeChecked `
    -Command {
      python `
        ".\phase159_pi4_3_repair3c_fix1_provider_key_chain_only\apply_phase159_repair3c_fix1.py"
    } `
    -FailureMessage "repair3c fix1 apply failed"

  Write-Host ""
  Write-Host "[2/5] Compile changed production file and new test"
  Invoke-NativeChecked `
    -Command {
      python -m py_compile `
        ".\toda_group_proof_narrative_contribution_ordering.py" `
        ".\tests\test_phase159_pi4_3_repair3c_fix1_provider_key_chain_only.py"
    } `
    -FailureMessage "repair3c fix1 compile check failed"

  Write-Host ""
  Write-Host "[3/5] Run fix1 structural regression"
  Invoke-NativeChecked `
    -Command {
      python -m pytest -q `
        ".\tests\test_phase159_pi4_3_repair3c_fix1_provider_key_chain_only.py"
    } `
    -FailureMessage "repair3c fix1 structural regression failed"

  Write-Host ""
  Write-Host "[4/5] Run pi_4^3 repair3c focused regression"
  Invoke-NativeChecked `
    -Command {
      python -m pytest -q `
        ".\tests\test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py"
    } `
    -FailureMessage "pi_4^3 repair3c regression failed"

  Write-Host ""
  Write-Host "[5/5] Run contribution-ordering focused regression"
  Invoke-NativeChecked `
    -Command {
      python -m pytest -q `
        ".\tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py" `
        ".\tests\test_phase149_rc3_3_minimal_ordering.py"
    } `
    -FailureMessage "contribution-ordering focused regression failed"
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3c fix1 focused verification complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
