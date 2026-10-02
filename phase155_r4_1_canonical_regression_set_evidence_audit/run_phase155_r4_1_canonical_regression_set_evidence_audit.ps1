$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R4-1 - canonical regression set evidence audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion/move/marker changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv",
  "tests"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155 input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R4-1 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r4_1.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-1 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Classify current tests and collect canonical candidates"
Write-Host "    No test execution beyond collect-only."

python `
  "$PackageDir\audit_phase155_r4_1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R4-1 evidence audit failed."
}

Write-Host ""
Write-Host "Phase 155-R4-1 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r4_1_audit_output\phase155_r4_1_summary.md"
Write-Host "Classification: $RepoRoot\phase155_r4_1_audit_output\phase155_r4_1_test_classification.csv"
Write-Host "Next: Phase 155-R4-2 canonical boundary validation"
