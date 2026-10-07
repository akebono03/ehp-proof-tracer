$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair3a audit"
Write-Host "Contribution selection internals only"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Push-Location $RepoRoot
try {
  Write-Host "[1/1] Audit contribution selection internals"
  python `
    ".\phase159_pi4_3_repair3a_contribution_selection_audit\audit_phase159_pi4_3_repair3a.py"

  if ($LASTEXITCODE -ne 0) {
    throw "repair3a audit failed with exit code $LASTEXITCODE"
  }
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3a audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
