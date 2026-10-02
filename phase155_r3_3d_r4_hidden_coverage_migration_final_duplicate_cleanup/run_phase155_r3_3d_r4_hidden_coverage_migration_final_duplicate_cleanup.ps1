$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3D-r4 - hidden coverage migration / final duplicate cleanup"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Changed surface: tests only"
Write-Host "Production changes: none"
Write-Host "Import changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

$Required = @(
  "phase155_r3_3d_r2_audit_output\phase155_r3_3d_r2_duplicate_semantics.json",
  "phase155_r3_3d_r3_audit_output\phase155_r3_3d_r3_hidden_coverage.json",
  "phase155_r3_3d_r3_audit_output\phase155_r3_3d_r3_pair_decisions.json",
  "phase155_r3_3a_audit_output\phase155_r3_3a_nodes.csv",
  "phase155_r3_2f_r1_audit_output\phase155_r3_2f_r1_verified_pairs.csv",
  "phase155_r3_3b_audit_output\phase155_r3_3b_candidate_safety.csv"
)

foreach ($RelativePath in $Required) {
  $FullPath = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path $FullPath)) {
    throw "Required Phase 155 audit input not found: $FullPath"
  }
}

Write-Host "1/3 Focused tests for the R3-3D-r4 cleanup/verification tools"

python -m pytest `
  "$PackageDir\test_phase155_r3_3d_r4_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r4 tool tests failed."
}

Write-Host ""
Write-Host "2/3 Apply audited test-only cleanup"
Write-Host "    - activate hidden coverage by renaming shadowed tests"
Write-Host "    - remove cleanup-ready shadowed definitions"
Write-Host "    - remove the two audited older pair tests"

python `
  "$PackageDir\apply_phase155_r3_3d_r4.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r4 cleanup failed."
}

Write-Host ""
Write-Host "3/3 Verify focused tests and repaired R3 closure conditions"
Write-Host "    Repository-wide pytest is still deferred to Phase 155 closure."

python `
  "$PackageDir\verify_phase155_r3_3d_r4.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3D-r4 repaired closure verification failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3D-r4 completed."
Write-Host "Production changes: none"
Write-Host "Import changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Cleanup manifest: $RepoRoot\phase155_r3_3d_r4_cleanup_output\phase155_r3_3d_r4_cleanup_manifest.json"
Write-Host "Closure summary: $RepoRoot\phase155_r3_3d_r4_verification_output\phase155_r3_3d_r4_summary.md"
Write-Host "Next: Phase 155-R4 canonical regression set"
