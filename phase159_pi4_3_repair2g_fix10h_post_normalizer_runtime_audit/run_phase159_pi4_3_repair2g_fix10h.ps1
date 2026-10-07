$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - repair2g fix10h audit"
Write-Host "Post-normalizer runtime contract trace"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/1] Inspect runtime contract and sentinel flow"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix10h.py"
if ($LASTEXITCODE -ne 0) {
  throw "fix10h runtime audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "fix10h audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
