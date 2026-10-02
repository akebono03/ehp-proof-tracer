$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R4 - final historical-heavy cleanup"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Reviewed partition of remaining 14:"
Write-Host "  DELETE:              10"
Write-Host "  LIGHTWEIGHT_REPLACE:  2"
Write-Host "  KEEP_AUDIT_ONLY:       2"
Write-Host ""
Write-Host "No heavy audit will run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""

Write-Host "1/3 Lightweight R2B-R4 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2b_r4_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R4 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply final historical-heavy cleanup"

python `
  "$PackageDir\apply_phase155_closure_r2b_r4.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R4 repository update failed."
}

Write-Host ""
Write-Host "3/3 Run only lightweight replacements and boundary tests"

python `
  "$PackageDir\verify_phase155_closure_r2b_r4.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R4 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R4 COMPLETE"
Write-Host "=============================================================="
Write-Host "Historical tests deleted: 10"
Write-Host "Heavy tests lightweight-replaced: 2"
Write-Host "Audit-only tests retained: 2"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
