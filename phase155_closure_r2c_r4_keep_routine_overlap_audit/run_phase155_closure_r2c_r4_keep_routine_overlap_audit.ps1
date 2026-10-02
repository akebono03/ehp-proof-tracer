$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R4 - KEEP_ROUTINE overlap audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is STATIC."
Write-Host "No KEEP_ROUTINE_CANDIDATE test body will run."
Write-Host "No repository file will be modified."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/2 Lightweight R2C-R4 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2c_r4_audit.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R4 tooling tests failed."
}

Write-Host ""
Write-Host "2/2 Static assertion-level overlap/redundancy audit"

python `
  "$PackageDir\phase155_closure_r2c_r4_audit.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2C-R4 static audit failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2C-R4 COMPLETE"
Write-Host "=============================================================="
Write-Host "Repository tests executed: 0"
Write-Host "Repository files changed: 0"
Write-Host "Production changes: none"
Write-Host ""
Write-Host "Report:"
Write-Host "  $RepoRoot\phase155_closure_r2c_r4_output\phase155_closure_r2c_r4_audit.md"
