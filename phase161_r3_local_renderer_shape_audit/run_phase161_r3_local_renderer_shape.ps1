$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R3 - local renderer shape audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

python `
  ".\phase161_r3_local_renderer_shape_audit\audit_phase161_r3_local_renderer_shape.py"

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed."
Write-Host "Production code changes: none"
Write-Host "Output:"
Write-Host "  .\phase161_r3_local_renderer_shape_audit\output\phase161_r3_local_renderer_shape.txt"
Write-Host "=============================================================="
