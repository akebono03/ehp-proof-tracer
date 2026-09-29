$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir
$Payload = Join-Path $PhaseDir "payload"

Copy-Item `
  -Path (Join-Path $Payload "toda_group_proof_narrative_contribution_ordering.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_ordering.py") `
  -Force

Copy-Item `
  -Path (Join-Path $Payload "tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py") `
  -Force

Write-Host "Phase 144-6-R5-42-R1 occurrence-downstream repair applied."
Write-Host "Expected production contribution population: 190."
Write-Host "Renderer/public output changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  pytest -q `
    ".\tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
