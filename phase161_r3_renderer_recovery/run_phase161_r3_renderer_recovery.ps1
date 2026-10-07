$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R3 - renderer recovery"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Recover production renderer from original R3 backup"
python `
  ".\phase161_r3_renderer_recovery\recover_phase161_r3_renderer.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Compile recovered renderer"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Inspect recovered renderer shape"
python `
  ".\phase161_r3_renderer_recovery\inspect_recovered_renderer.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Re-run pre-R3 focused regressions"
python -m pytest -q `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py" `
  ".\tests\test_phase157_r20_repair12_map_property_reference_support.py" `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Renderer recovery completed."
Write-Host "Phase 161-R3 feature repair: NOT APPLIED"
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
