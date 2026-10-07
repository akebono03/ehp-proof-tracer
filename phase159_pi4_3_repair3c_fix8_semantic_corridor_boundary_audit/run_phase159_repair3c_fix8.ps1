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
Write-Host "Phase 159 - pi_4^3 repair3c fix8 semantic corridor audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Push-Location $RepoRoot
try {
  Write-Host "[1/2] Run semantic corridor boundary audit"
  Invoke-NativeChecked `
    -Command {
      python `
        ".\phase159_pi4_3_repair3c_fix8_semantic_corridor_boundary_audit\audit_phase159_repair3c_fix8.py"
    } `
    -FailureMessage "repair3c fix8 audit failed"

  Write-Host ""
  Write-Host "[2/2] Re-run historical upstream boundary tests"
  Invoke-NativeChecked `
    -Command {
      python -m pytest -q `
        ".\tests\test_phase144_6_r5_30_upstream_calculation_attachment_audit.py"
    } `
    -FailureMessage "historical upstream boundary test failed"
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3c fix8 audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
