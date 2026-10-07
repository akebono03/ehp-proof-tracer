$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair3 audit"
Write-Host "Proof-body exposure pipeline"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/1] Audit raw -> closure -> blocks -> local body -> contributions -> public"
python "$PackageRoot\audit_phase159_pi4_3_repair3_body_exposure.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair3 body exposure audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair3 body exposure audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
