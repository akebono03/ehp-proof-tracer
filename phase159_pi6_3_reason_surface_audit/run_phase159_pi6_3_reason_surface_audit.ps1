$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi6_3 reason surface audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

python "$ScriptDir\audit_phase159_pi6_3_reason_surface.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}
