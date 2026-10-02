$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R1 - CONTRACT_SENSITIVE static review"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is STATIC and LIGHTWEIGHT."
Write-Host "No CONTRACT_SENSITIVE repository test body will run."
Write-Host "No repository file will be modified."
Write-Host "The known 508s / 281s / 276s tests will NOT run."
Write-Host ""

Write-Host "1/2 Lightweight R2C-R1 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2c_r1_audit.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/2 Static review of the 24 CONTRACT_SENSITIVE nodeids"

python `
  "$PackageDir\phase155_closure_r2c_r1_audit.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R1 static review failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Repository tests executed: 0"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host ""
Write-Host "Report:"
Write-Host "  $RepoRoot\phase155_closure_r2c_r1_output\phase155_closure_r2c_r1_review.md"
