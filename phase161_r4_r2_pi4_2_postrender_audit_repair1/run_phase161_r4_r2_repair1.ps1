$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R2 repair1 - pi_4^2 post-render audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/2] Validate current Phase 161-R4 production files"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py" `
  ".\toda_group_proof_narrative_references.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Audit full pi_4^2 Reference/body state"
python `
  ".\phase161_r4_r2_pi4_2_postrender_audit_repair1\audit_phase161_r4_r2_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed."
Write-Host "Production changes: NONE"
Write-Host "Tests changed: NONE"
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
