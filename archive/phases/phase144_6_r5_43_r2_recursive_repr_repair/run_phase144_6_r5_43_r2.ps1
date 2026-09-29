$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir
$Payload = Join-Path $PhaseDir "payload"

Copy-Item `
  -Path (Join-Path $Payload "toda_group_proof_narrative_contribution_ordering.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_ordering.py") `
  -Force

Copy-Item `
  -Path (Join-Path $Payload "toda_group_proof_narrative_contribution_renderer.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py") `
  -Force

Copy-Item `
  -Path (Join-Path $Payload "tests\test_phase144_6_r5_43_generic_renderer_contribution_connection.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_generic_renderer_contribution_connection.py") `
  -Force

Copy-Item `
  -Path (Join-Path $Payload "tests\test_phase144_6_r5_43_r2_recursive_repr_repair.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_r2_recursive_repr_repair.py") `
  -Force

Write-Host "Phase 144-6-R5-43-R2 recursive repr repair applied."
Write-Host "Production grouping no longer calls repr(proof_step.conclusion)."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host "1/3 R5-43-R2 safety/population tests"
  pytest -q `
    ".\tests\test_phase144_6_r5_43_r2_recursive_repr_repair.py"

  Write-Host "2/3 R5-42 production foundation regression"
  pytest -q `
    ".\tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py"

  Write-Host "3/3 R5-43 renderer connection"
  pytest -q `
    ".\tests\test_phase144_6_r5_43_generic_renderer_contribution_connection.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
