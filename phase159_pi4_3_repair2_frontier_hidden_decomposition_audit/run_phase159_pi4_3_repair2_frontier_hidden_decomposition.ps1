$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2 frontier-hidden decomposition audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Run frontier-hidden decomposition audit"
python "$PackageRoot\audit_phase159_pi4_3_repair2_frontier_hidden_decomposition.py"
if ($LASTEXITCODE -ne 0) {
  throw "frontier-hidden audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/2] Run focused Narrative tests"
python -m pytest `
  tests/test_phase143_36_argument_body_blocks.py `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "focused Narrative tests failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
