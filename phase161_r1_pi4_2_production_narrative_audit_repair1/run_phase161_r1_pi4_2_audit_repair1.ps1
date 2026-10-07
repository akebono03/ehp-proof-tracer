$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$OutputDir = Join-Path $PackageDir "output"
$AuditOutput = Join-Path $OutputDir "phase161_r1_pi4_2_audit.txt"

New-Item `
  -ItemType Directory `
  -Path $OutputDir `
  -Force | Out-Null

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R1 repair1 - pi_4^2 production proof / Narrative audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/3] Production proof and Narrative audit"
python `
  ".\phase161_r1_pi4_2_production_narrative_audit_repair1\audit_phase161_r1_pi4_2.py" `
  2>&1 | Tee-Object -FilePath $AuditOutput
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/3] Existing focused Phase 59 regression tests"
python -m pytest -q `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/3] Existing Phase 160 k=2 transport regression tests"
python -m pytest -q `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R1 repair1 audit completed."
Write-Host "Production code changes: none"
Write-Host "Audit output:"
Write-Host "  $AuditOutput"
Write-Host "=============================================================="
