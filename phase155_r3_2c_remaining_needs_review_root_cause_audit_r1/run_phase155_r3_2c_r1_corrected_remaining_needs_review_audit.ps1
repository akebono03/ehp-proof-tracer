$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-2C-r1 - corrected remaining needs-review audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Correction: includes source_evidence_issue AND other_review_reason"
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_2_audit_output\phase155_r3_2_verified_pairs.csv",
  "phase155_r3_2_audit_output\phase155_r3_2_source_evidence.csv",
  "phase155_r3_2b_audit_output\phase155_r3_2b_needs_review_audit.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required audit input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the corrected R3-2C audit tool only"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_2c.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2C-r1 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Classify all six non-failure-linked needs-review pairs"

python `
  "$PackageDir\audit_phase155_r3_2c.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-2C-r1 audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-2C-r1 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_2c_r1_audit_output\phase155_r3_2c_r1_summary.md"
Write-Host "Root causes: $RepoRoot\phase155_r3_2c_r1_audit_output\phase155_r3_2c_r1_root_causes.csv"
