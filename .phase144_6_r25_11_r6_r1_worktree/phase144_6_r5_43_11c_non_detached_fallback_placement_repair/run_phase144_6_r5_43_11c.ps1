$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Copy-Item `
  -Path (Join-Path $PhaseDir "toda_group_proof_narrative_contribution_renderer.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py") `
  -Force

Write-Host "Phase 144-6-R5-43-11C non-DETACHED fallback placement repair applied."
Write-Host "Production change: contribution renderer fallback placement only."
Write-Host "Public CLI/Web renderer route changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  Write-Host "1/3 R5-43-11C focused repair tests"
  pytest -q ".\tests\test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "2/3 R5-43-2 placement regression"
  pytest -q ".\tests\test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "3/3 R5-43-10 transport compression regression"
  pytest -q ".\tests\test_phase144_6_r5_43_10_transport_chain_compression_production.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
