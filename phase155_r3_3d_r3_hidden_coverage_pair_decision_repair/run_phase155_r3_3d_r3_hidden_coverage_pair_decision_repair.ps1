$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3D-r3 - hidden coverage preservation / pair decision repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_3d_r2_audit_output\phase155_r3_3d_r2_duplicate_semantics.json",
  "phase155_r3_3d_r2_audit_output\phase155_r3_3d_r2_unresolved_pair_semantics.json",
  "phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required audit input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R3-3D-r3 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_3d_r3.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r3 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Audit hidden coverage and repair unresolved-pair decisions"

python `
  "$PackageDir\audit_phase155_r3_3d_r3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r3 audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3D-r3 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_3d_r3_audit_output\phase155_r3_3d_r3_summary.md"
Write-Host "Repair plan: $RepoRoot\phase155_r3_3d_r3_audit_output\phase155_r3_3d_r3_repair_plan.json"
