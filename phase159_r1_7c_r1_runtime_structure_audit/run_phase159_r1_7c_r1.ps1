$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7c R1 - runtime structure audit"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7c_r1_runtime_structure_audit"
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host "Production code changes: none"
  Write-Host "Test changes: none"
  Write-Host ""

  Write-Host "[1/2] Syntax preflight"
  python -m py_compile `
    (Join-Path $PhaseDir "audit_phase159_r1_7c_r1.py")
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host ""
  Write-Host "[2/2] Run R1 structure audit"
  python (Join-Path $PhaseDir "audit_phase159_r1_7c_r1.py")
  if ($LASTEXITCODE -ne 0) {
    throw "R1 structure audit failed"
  }

  Write-Host ""
  Write-Host "Audit completed."
  Write-Host "No production files changed."
  Write-Host "No tests changed."
  Write-Host "No pytest run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
