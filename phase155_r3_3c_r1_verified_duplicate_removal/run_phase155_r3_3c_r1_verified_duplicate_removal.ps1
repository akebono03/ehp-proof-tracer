$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3C-r1 - verified duplicate removal repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This repair first restores the failed R3-3C partial application"
Write-Host "from its timestamped sibling backup."
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Expected safe test IDs removed: 161"
Write-Host "Expected whole test-file deletions: 5"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_3a_audit_output\phase155_r3_3a_nodes.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_candidate_safety.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_file_safety.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required R3-3 input not found: $FullPath"
  }
}

Write-Host "1/4 Focused tests for the repaired removal/verification tools"

python -m pytest `
  "$PackageDir\test_phase155_r3_3c_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r1 tool tests failed."
}

Write-Host ""
Write-Host "2/4 Restore failed partial application, preflight all targets, then apply"

python `
  "$PackageDir\apply_phase155_r3_3c_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r1 removal failed."
}

Write-Host ""
Write-Host "3/4 Verify removed IDs, survivors, affected files, and importers"
Write-Host "    This runs focused pytest only."

python `
  "$PackageDir\verify_phase155_r3_3c_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r1 focused verification failed."
}

Write-Host ""
Write-Host "4/4 Git diff summary"

git status --short
git diff --stat

Write-Host ""
Write-Host "Phase 155-R3-3C-r1 completed."
Write-Host "Production changes: none"
Write-Host "Removed duplicate test IDs: 161"
Write-Host "Whole test files deleted: 5"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Manifest: $RepoRoot\phase155_r3_3c_r1_removal_output\phase155_r3_3c_r1_removal_manifest.json"
Write-Host "Verification: $RepoRoot\phase155_r3_3c_r1_removal_output\phase155_r3_3c_r1_verification.json"
