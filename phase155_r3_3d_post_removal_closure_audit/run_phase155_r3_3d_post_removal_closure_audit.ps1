$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3D - post-removal closure audit"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv",
  "phase155_r3_3a_audit_output\phase155_r3_3a_nodes.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_candidate_safety.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_file_safety.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required R3 audit input not found: $FullPath"
  }
}

Write-Host "1/2 Focused tests for the R3-3D closure tool"

python -m pytest `
  "$PackageDir\test_audit_phase155_r3_3d.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D audit-tool tests failed."
}

Write-Host ""
Write-Host "2/2 Audit post-removal source, pair closure, survivors, historical protection, and focused collection"
Write-Host "    This does NOT run repository-wide pytest."

python `
  "$PackageDir\audit_phase155_r3_3d.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D closure conditions were not satisfied."
}

Write-Host ""
Write-Host "Phase 155-R3-3D completed."
Write-Host "Production changes: none"
Write-Host "Existing-test changes: none"
Write-Host "Test deletion: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Summary: $RepoRoot\phase155_r3_3d_audit_output\phase155_r3_3d_summary.md"
Write-Host "Metadata: $RepoRoot\phase155_r3_3d_audit_output\phase155_r3_3d_metadata.json"
