$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R5 - heavy / historical boundary"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This R5 audit is LIGHTWEIGHT."
Write-Host "It performs static source analysis only."
Write-Host "No test bodies are executed."
Write-Host "Checkpoint/resume is enabled."
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion/move/marker changes: none"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r4_4_audit_output\phase155_r4_4_final_classification.csv",
  "tests"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155-R4-4 input not found: $FullPath"
  }
}

Write-Host "1/2 Lightweight unit tests for the R5 classifier"

python -m pytest `
  "$PackageDir\test_audit_phase155_r5.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R5 classifier tests failed."
}

Write-Host ""
Write-Host "2/2 Static boundary classification"
Write-Host "    Progress is shown for every file."
Write-Host "    Completed files are checkpointed and skipped on rerun."

python `
  "$PackageDir\audit_phase155_r5.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R5 boundary audit failed."
}

Write-Host ""
Write-Host "Phase 155-R5 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test bodies: NOT run"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r5_audit_output\phase155_r5_summary.md"
Write-Host "Classification: $RepoRoot\phase155_r5_audit_output\phase155_r5_boundary_classification.csv"
Write-Host ""
Write-Host "Next: Phase 155-R6 pytest collection / runtime audit"
