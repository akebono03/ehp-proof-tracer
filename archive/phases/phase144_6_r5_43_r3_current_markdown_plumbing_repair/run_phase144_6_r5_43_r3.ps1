$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir
$Payload = Join-Path $PhaseDir "payload"

Copy-Item (Join-Path $Payload "toda_group_proof_narrative_contribution_ordering.py") (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_ordering.py") -Force
Copy-Item (Join-Path $Payload "toda_group_proof_narrative_contribution_renderer.py") (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py") -Force
Copy-Item (Join-Path $Payload "tests\\test_phase144_6_r5_43_generic_renderer_contribution_connection.py") (Join-Path $RepoRoot "tests\\test_phase144_6_r5_43_generic_renderer_contribution_connection.py") -Force
Copy-Item (Join-Path $Payload "tests\\test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py") (Join-Path $RepoRoot "tests\\test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py") -Force

Write-Host "Phase 144-6-R5-43-R3 current_markdown plumbing repair applied."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host "1/3 plumbing tests"
  pytest -q ".\\tests\\test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "2/3 R5-42 regression"
  pytest -q ".\\tests\\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "3/3 R5-43 renderer connection"
  pytest -q ".\\tests\\test_phase144_6_r5_43_generic_renderer_contribution_connection.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
