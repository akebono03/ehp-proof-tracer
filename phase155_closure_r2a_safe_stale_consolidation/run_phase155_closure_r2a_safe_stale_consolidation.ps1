$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2A - SAFE_STALE consolidation"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is FOCUSED and checkpointed."
Write-Host "Repository-wide pytest will NOT run."
Write-Host "38 SAFE_STALE tests are split into 4 batches."
Write-Host "PASS batches are reused on rerun."
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Import changes: none"
Write-Host "Phase144 / Phase153 / Phase95-98: not changed"
Write-Host ""

Write-Host "1/3 Lightweight R2A tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2a_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2A tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Apply 38 test-expectation repairs"

python `
  "$PackageDir\repair_phase155_closure_r2a.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2A source repair failed."
}

Write-Host ""
Write-Host "3/3 Run only the 38 repaired tests in checkpointed batches"
Write-Host "The Phase143 semantic batch is a little heavy."
Write-Host "The 10,421-test repository suite is not executed."
Write-Host ""

python `
  "$PackageDir\run_phase155_closure_r2a_focused.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2A focused verification failed. PASS checkpoints are preserved."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2A COMPLETE"
Write-Host "=============================================================="
Write-Host "SAFE_STALE repaired: 38"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""
Write-Host "Next: Closure-R2B - HISTORICAL_HEAVY 36 runtime/redundancy review"
