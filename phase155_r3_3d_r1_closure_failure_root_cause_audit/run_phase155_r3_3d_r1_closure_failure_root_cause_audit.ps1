$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3D-r1 - closure failure root-cause audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_3d_audit_output\phase155_r3_3d_pair_closure.csv",
  "phase155_r3_3d_audit_output\phase155_r3_3d_duplicate_definitions.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required R3-3D output not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R3-3D-r1 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_3d_r1.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r1 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Classify 2 unresolved pairs and 8 duplicate-name groups"

python `
  "$PackageDir\audit_phase155_r3_3d_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r1 root-cause audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3D-r1 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_3d_r1_audit_output\phase155_r3_3d_r1_summary.md"
