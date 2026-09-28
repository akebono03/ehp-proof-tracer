$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Copy-Item `
  -Path (Join-Path $PhaseDir "toda_group_proof_narrative_hidden_bridge_semantics.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_hidden_bridge_semantics.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "toda_group_proof_narrative_contribution_renderer.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "test_phase144_6_r5_43_10_transport_chain_compression_production.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_10_transport_chain_compression_production.py") `
  -Force

Write-Host "Phase 144-6-R5-43-10 transport-chain compression production changes applied."
Write-Host "Public CLI/Web renderer route changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  Write-Host "1/3 R5-43-10 focused production tests"
  pytest -q ".\tests\test_phase144_6_r5_43_10_transport_chain_compression_production.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "2/3 R5-43-7 semantic regression"
  pytest -q ".\tests\test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "3/3 R5-43-4 direct connector regression"
  pytest -q ".\tests\test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
