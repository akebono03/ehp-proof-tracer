$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi6_3 zero-map outer-stage audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

python "$ScriptDir\audit_phase159_pi6_3_zero_map_outer_stages.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "$ScriptDir\phase159_pi6_3_zero_map_outer_stage_audit.txt"
