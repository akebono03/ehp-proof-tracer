$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 exactness reason locality audit8"
Write-Host "No production changes"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

python (Join-Path $PackageDir "audit_phase159_pi3_2_exactness_reason_locality_audit8.py")

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "FAILED: audit8"
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Audit8 finished."
Write-Host "No production files or tests were changed."
Write-Host "Full suite was not run."
