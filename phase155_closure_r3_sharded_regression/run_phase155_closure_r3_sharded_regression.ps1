$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $RepoRoot "phase155_closure_r3_output"
$PlanPath = Join-Path $OutputDir "shard_plan.json"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3 - final sharded regression"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Policy:"
Write-Host "  shards: 8"
Write-Host "  target: about 5 minutes per shard"
Write-Host "  hard timeout: 10 minutes per shard"
Write-Host "  audit-only tests: excluded"
Write-Host "  passed shards: checkpointed and skipped on rerun"
Write-Host "  monolithic repository-wide pytest: NOT used"
Write-Host ""

Write-Host "1/3 Lightweight Closure-R3 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r3_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R3 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Collect routine tests and build weighted contiguous shard plan"

python `
  "$PackageDir\prepare_phase155_closure_r3.py" `
  --repo-root "$RepoRoot" `
  --package-dir "$PackageDir" `
  --output-dir "$OutputDir" `
  --shard-count 8

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R3 shard planning failed."
}

Write-Host ""
Write-Host "3/3 Execute shards with checkpoint/resume"

python `
  "$PackageDir\run_phase155_closure_r3.py" `
  --repo-root "$RepoRoot" `
  --package-dir "$PackageDir" `
  --plan "$PlanPath" `
  --output-dir "$OutputDir" `
  --timeout-seconds 600

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "Closure-R3 is INCOMPLETE."
  Write-Host "Passed shards are preserved in checkpoint.json."
  Write-Host "After fixing failures, run this same script again."
  throw "Closure-R3 has failing or timed-out shards."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3 COMPLETE"
Write-Host "=============================================================="
Write-Host "All routine shards: PASS"
Write-Host "Audit-only tests executed: 0"
Write-Host "Monolithic repository-wide pytest: NOT run"
Write-Host ""
Write-Host "Summary:"
Write-Host "  $OutputDir\summary.txt"
