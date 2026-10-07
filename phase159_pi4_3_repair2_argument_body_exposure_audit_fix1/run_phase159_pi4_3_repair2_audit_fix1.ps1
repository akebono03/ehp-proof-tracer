$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2 audit fix1"
Write-Host "Correct method-evidence import"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/3] Apply audit fix1"
python "$PackageRoot\apply_phase159_pi4_3_repair2_audit_fix1.py"
if ($LASTEXITCODE -ne 0) {
  throw "audit fix1 apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/3] Compile corrected audit"
python -m py_compile `
  ".\phase159_pi4_3_repair2_argument_body_exposure_audit\audit_phase159_pi4_3_repair2_argument_body_exposure.py"
if ($LASTEXITCODE -ne 0) {
  throw "corrected audit compile failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/3] Re-run repair2 Argument body exposure audit"
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_pi4_3_repair2_argument_body_exposure_audit\run_phase159_pi4_3_repair2_argument_body_exposure.ps1"
if ($LASTEXITCODE -ne 0) {
  throw "corrected repair2 audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair2 audit fix1 complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
