$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $RepoRoot "phase155_closure_r3_output"
$PlanPath = Join-Path $OutputDir "shard_plan.json"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3-R1 - runner syntax repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This repair does NOT recollect tests."
Write-Host "This repair reuses the existing 8-shard plan."
Write-Host "Repository files will NOT be modified."
Write-Host "Audit-only tests remain excluded."
Write-Host "Hard timeout remains 10 minutes per shard."
Write-Host ""

Write-Host "1/3 Lightweight repaired-runner tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r3_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R3-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/3 Validate and reuse the existing shard plan"

python `
  "$PackageDir\phase155_closure_r3_r1_validate.py" `
  --repo-root "$RepoRoot" `
  --plan "$PlanPath"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R3-R1 existing shard-plan validation failed."
}

Write-Host ""
Write-Host "3/3 Execute existing shards with the repaired runner"

python `
  "$PackageDir\run_phase155_closure_r3_fixed.py" `
  --repo-root "$RepoRoot" `
  --package-dir "$PackageDir" `
  --plan "$PlanPath" `
  --output-dir "$OutputDir" `
  --timeout-seconds 600

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "Closure-R3 remains INCOMPLETE."
  Write-Host "PASS shards are preserved in checkpoint.json."
  Write-Host "After repairing only failing shards, rerun this same R3-R1 script."
  throw "Closure-R3 has failing or timed-out shards."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Existing collection reused: yes"
Write-Host "All routine shards: PASS"
Write-Host "Audit-only tests executed: 0"
Write-Host "Monolithic repository-wide pytest: NOT run"
Write-Host ""
Write-Host "Summary:"
Write-Host "  $OutputDir\summary.txt"
