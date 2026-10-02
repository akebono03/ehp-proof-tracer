$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R6 - pytest collection / runtime audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "IMPORTANT: this can be MODERATELY HEAVY."
Write-Host "Collection covers the current test files in checkpointed batches."
Write-Host "Runtime execution is bounded to a small deterministic probe set."
Write-Host "Progress is printed for every collection batch and runtime probe."
Write-Host "Completed work is checkpointed and skipped on rerun."
Write-Host ""
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r5_audit_output\phase155_r5_canonical_routine_nodeids.txt",
  "phase155_r5_audit_output\phase155_r5_historical_nodeids.txt",
  "phase155_r5_audit_output\phase155_r5_audit_only_nodeids.txt",
  "phase155_r5_audit_output\phase155_r5_heavy_nodeids.txt",
  "phase155_r5_audit_output\phase155_r5_residual_retained_nodeids.txt"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155-R5 input not found: $FullPath"
  }
}

Write-Host "1/2 Lightweight unit tests for the R6 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r6.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R6 tool tests failed."
}

Write-Host ""
Write-Host "2/2 Checkpointed collection + bounded runtime probe"

python `
  "$PackageDir\audit_phase155_r6.py" `
  --repo-root "$RepoRoot" `
  --runtime-timeout 60

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R6 audit failed."
}

Write-Host ""
Write-Host "Phase 155-R6 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r6_audit_output\phase155_r6_summary.md"
Write-Host ""
Write-Host "Next: Phase 155 closure planning."
Write-Host "The repository-wide full pytest remains reserved for Phase 155 closure."
