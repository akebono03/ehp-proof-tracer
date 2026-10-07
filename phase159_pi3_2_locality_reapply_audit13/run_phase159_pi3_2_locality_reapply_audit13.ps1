$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 locality re-apply audit13"
Write-Host "No production changes"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

python (Join-Path $PackageDir "audit_phase159_pi3_2_locality_reapply_audit13.py")

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "FAILED: audit13"
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Audit13 finished."
Write-Host "No production files or tests were changed."
Write-Host "Full suite was not run."
