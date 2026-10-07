$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7c R2 repair4 - projected match diagnosis"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7c_r2_repair4_projected_match_diagnosis"
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host "Production code changes: none"
  Write-Host "Test changes: none"
  Write-Host ""

  Write-Host "[1/2] Syntax preflight"
  python -m py_compile `
    (Join-Path $PhaseDir "audit_phase159_r1_7c_r2_repair4.py")
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host ""
  Write-Host "[2/2] Run diagnosis"
  python (Join-Path $PhaseDir "audit_phase159_r1_7c_r2_repair4.py")
  if ($LASTEXITCODE -ne 0) {
    throw "diagnosis failed"
  }

  Write-Host ""
  Write-Host "Diagnosis completed."
  Write-Host "No production files changed."
  Write-Host "No tests changed."
  Write-Host "No pytest run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
