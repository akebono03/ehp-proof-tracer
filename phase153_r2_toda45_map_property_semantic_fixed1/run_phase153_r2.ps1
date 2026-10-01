$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = (Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 153-R2 Fixed1"
Write-Host "Toda45IsomorphismStatement -> MAP_PROPERTY"
Write-Host "Generic isomorphism rendering reuse"
Write-Host "=============================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepositoryRoot "toda_group_proof_narrative_blocks.py"))) {
  throw "Run this script from the ehp-proof-tracer repository root."
}

Write-Host "A. Applying minimal Phase153-R2 production change..."
python (Join-Path $PackageRoot "apply_phase153_r2.py")
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "B. Syntax check..."
python -m py_compile `
  .\toda_group_proof_narrative_blocks.py `
  .\toda_group_proof_generic_narrative_renderer.py `
  .\tests\test_phase153_r2_toda45_map_property_semantic.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "C. Existing Toda 4.5 theorem semantics regression..."
pytest -q `
  tests/test_phase46_toda_45_theorem_semantics.py `
  tests/test_phase143_75c_generic_semantic_rendering.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "D. Phase153-R2 focused regression..."
pytest -q `
  tests/test_phase153_r2_toda45_map_property_semantic.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase153-R2 Fixed1 focused checks passed."
Write-Host "Whole repository pytest was NOT run."
Write-Host "=============================================================="
