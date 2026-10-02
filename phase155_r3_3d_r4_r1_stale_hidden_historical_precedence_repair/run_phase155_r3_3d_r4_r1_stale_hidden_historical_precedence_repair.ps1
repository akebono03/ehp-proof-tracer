$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3D-r4-r1 - stale hidden / historical precedence repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Changed surface: tests only"
Write-Host "Production changes: none"
Write-Host "Import changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_3d_r4_cleanup_output\phase155_r3_3d_r4_cleanup_manifest.json",
  "phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_candidate_safety.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155 audit input not found: $FullPath"
  }
}

Write-Host "1/3 Focused tests for the r4-r1 repair tool"

python -m pytest `
  "$PackageDir\test_phase155_r3_3d_r4_r1_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r4-r1 tool tests failed."
}

Write-Host ""
Write-Host "2/3 Remove stale hidden tests and restore historical_keep tests"

python `
  "$PackageDir\apply_phase155_r3_3d_r4_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r4-r1 repair failed."
}

Write-Host ""
Write-Host "3/3 Focused pytest and repaired R3 closure verification"
Write-Host "    historical_keep takes precedence over removable_duplicate"
Write-Host "    when the same test ID participates in both classifications."

python `
  "$PackageDir\verify_phase155_r3_3d_r4_r1.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r4-r1 closure verification failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3D-r4-r1 completed."
Write-Host "Production changes: none"
Write-Host "Import changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Next: Phase 155-R4 canonical regression set"
