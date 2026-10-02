$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2A-R1 - Reference-name stale repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This repair is FOCUSED."
Write-Host "Only 5 previously failing Phase132/133 tests are changed."
Write-Host "The previous 7 PASS tests are not rerun."
Write-Host "Repository-wide pytest is NOT run."
Write-Host ""

Write-Host "1/3 Lightweight R1 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2a_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2A-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply five stale Reference-name repairs"

python `
  "$PackageDir\repair_phase155_closure_r2a_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2A-R1 repair failed."
}

Write-Host ""
Write-Host "3/3 Run only the five previously failing tests, then resume batches 2-4"
Write-Host "This avoids rerunning the previous 7 PASS tests."
Write-Host ""

python `
  "$PackageDir\run_phase155_closure_r2a_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2A-R1 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2A-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
