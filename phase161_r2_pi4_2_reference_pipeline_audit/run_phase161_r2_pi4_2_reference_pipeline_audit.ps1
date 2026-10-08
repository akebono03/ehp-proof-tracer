$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$OutputDir = Join-Path $PackageDir "output"
$AuditOutput = Join-Path $OutputDir "phase161_r2_pi4_2_reference_pipeline.txt"

New-Item `
  -ItemType Directory `
  -Path $OutputDir `
  -Force | Out-Null

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R2 - pi_4^2 Reference pipeline audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/2] Trace current Reference pipeline"
python `
  ".\phase161_r2_pi4_2_reference_pipeline_audit\audit_phase161_r2_pi4_2_reference_pipeline.py" `
  2>&1 | Tee-Object -FilePath $AuditOutput
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Re-run focused regression tests"
python -m pytest -q `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py" `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R2 audit completed."
Write-Host "Production code changes: none"
Write-Host "Audit output:"
Write-Host "  $AuditOutput"
Write-Host "=============================================================="
