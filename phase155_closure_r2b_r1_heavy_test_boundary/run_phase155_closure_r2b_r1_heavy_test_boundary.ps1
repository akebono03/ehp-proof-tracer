$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R1 - heavy-test boundary"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is LIGHTWEIGHT."
Write-Host "No Phase144 historical-heavy test body will run."
Write-Host "Repository-wide pytest will NOT run."
Write-Host ""
Write-Host "Implementation:"
Write-Host "  22 AUDIT_ONLY nodeids -> excluded from routine pytest"
Write-Host "   1 SPLIT_OR_CACHE nodeid -> excluded from routine pytest"
Write-Host "  23 total historical-heavy nodeids remain available by opt-in"
Write-Host ""

Write-Host "1/3 Lightweight installer self-tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2b_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Install audit-only collection boundary"

python `
  "$PackageDir\install_phase155_closure_r2b_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R1 install failed."
}

Write-Host ""
Write-Host "3/3 Run only the new lightweight boundary tests"

python -m pytest `
  "tests/test_phase155_audit_boundary.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2B-R1 boundary tests failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2B-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Historical-heavy nodeids removed from routine pytest: 23"
Write-Host "Historical audit coverage retained by opt-in: yes"
Write-Host "Production changes: none"
Write-Host "Phase144 existing test-body changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""
Write-Host "Explicit historical audit runner:"
Write-Host "  .\phase155_closure_r2b_r1_heavy_test_boundary\run_phase155_historical_audits.ps1"
