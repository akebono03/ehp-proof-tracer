$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 - repair3c fix1 performance audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Push-Location $RepoRoot
try {
  python `
    ".\phase159_pi4_3_repair3c_fix1_cross_group_performance_audit\audit_phase159_repair3c_fix1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "repair3c fix1 audit failed with exit code $LASTEXITCODE"
  }
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3c fix1 performance audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
