$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair3b audit"
Write-Host "Provider-anchor ancestry"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Push-Location $RepoRoot
try {
  Write-Host "[1/1] Audit provider-anchor upstream ancestry"
  python `
    ".\phase159_pi4_3_repair3b_provider_anchor_ancestry_audit\audit_phase159_pi4_3_repair3b.py"

  if ($LASTEXITCODE -ne 0) {
    throw "repair3b audit failed with exit code $LASTEXITCODE"
  }
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3b audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
