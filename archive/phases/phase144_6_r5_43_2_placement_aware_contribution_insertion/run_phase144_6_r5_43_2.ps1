$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir
$Payload = Join-Path $PhaseDir "payload"

Copy-Item (Join-Path $Payload "toda_group_proof_narrative_contribution_ordering.py") (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_ordering.py") -Force
Copy-Item (Join-Path $Payload "toda_group_proof_narrative_contribution_renderer.py") (Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py") -Force
Copy-Item (Join-Path $Payload "tests\\test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py") (Join-Path $RepoRoot "tests\\test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py") -Force
Copy-Item (Join-Path $PhaseDir "audit_phase144_6_r5_43_2.py") (Join-Path $RepoRoot "audit_phase144_6_r5_43_2.py") -Force

Write-Host "Phase 144-6-R5-43-2 placement-aware insertion applied."
Write-Host "Public renderer route changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  Write-Host "1/3 R5-43-2 placement tests"
  pytest -q ".\\tests\\test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "2/3 R5-42 production regression"
  pytest -q ".\\tests\\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "3/3 connected Narrative audit"
  python ".\\audit_phase144_6_r5_43_2.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
