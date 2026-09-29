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

Write-Host "Phase 144-6-R5-43 generic renderer contribution connection applied."
Write-Host "Existing public/base multi-Argument renderer remains unchanged."
Write-Host "New opt-in renderer: render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  pytest -q `
    ".\tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py" `
    ".\tests\test_phase144_6_r5_43_generic_renderer_contribution_connection.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
