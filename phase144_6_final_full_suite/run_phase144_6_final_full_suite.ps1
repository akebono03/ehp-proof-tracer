$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Full Suite"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""
Write-Host "Running the complete pytest suite exactly at the Phase boundary..."
Write-Host ""

$env:PYTHONPATH = $RepoRoot

pytest -q

$Code = $LASTEXITCODE
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

if ($Code -ne 0) {
  Write-Host ""
  Write-Host "Phase 144-6 final full suite: FAIL"
  exit $Code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 144-6 final full suite: PASS"
Write-Host "=============================================================="
Write-Host "Production changes in this package: none."
Write-Host "If this suite passes, Phase 144-6 implementation/test boundary is complete."
