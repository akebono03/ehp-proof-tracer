$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3D-r2 - divergent duplicate / unresolved pair semantic audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_3d_r1_audit_output\phase155_r3_3d_r1_duplicate_definitions.json",
  "phase155_r3_3d_r1_audit_output\phase155_r3_3d_r1_unresolved_pairs.json",
  "phase155_r3_3a_audit_output\phase155_r3_3a_nodes.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_candidate_safety.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required audit input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R3-3D-r2 audit tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_3d_r2.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r2 audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Audit runtime definition ownership, assertion coverage, and unresolved-pair mapping"

$env:PYTHONPATH = "$RepoRoot;$PackageDir"

python `
  "$PackageDir\audit_phase155_r3_3d_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r2 semantic audit failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3D-r2 completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_3d_r2_audit_output\phase155_r3_3d_r2_summary.md"
