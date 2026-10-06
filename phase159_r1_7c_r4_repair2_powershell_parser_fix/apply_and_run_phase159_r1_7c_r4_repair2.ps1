$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

$Source = Join-Path $PackageRoot "run_phase159_r1_7c_r4.ps1"
$TargetDir = Join-Path $RepoRoot "phase159_r1_7c_r4_cross_group_structural_audit"
$Target = Join-Path $TargetDir "run_phase159_r1_7c_r4.ps1"

if (-not (Test-Path $TargetDir)) {
  throw "Target R4 audit package was not found: $TargetDir"
}

Copy-Item -Path $Source -Destination $Target -Force

Write-Host "Phase 159 R1-7c R4 repair2 applied."
Write-Host "Replaced:"
Write-Host "  phase159_r1_7c_r4_cross_group_structural_audit\run_phase159_r1_7c_r4.ps1"
Write-Host ""
Write-Host "Now running repaired R4 audit."
Write-Host ""

& powershell -ExecutionPolicy Bypass -File $Target

if ($LASTEXITCODE -ne 0) {
  throw "Repaired Phase 159 R1-7c R4 audit failed with exit code $LASTEXITCODE."
}
