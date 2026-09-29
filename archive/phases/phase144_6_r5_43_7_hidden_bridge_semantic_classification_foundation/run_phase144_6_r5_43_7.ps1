$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Copy-Item `
  -Path (Join-Path $PhaseDir "payload\toda_group_proof_narrative_hidden_bridge_semantics.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_hidden_bridge_semantics.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "payload\tests\test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PhaseDir "audit_phase144_6_r5_43_7.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_43_7.py") `
  -Force

Write-Host "Phase 144-6-R5-43-7 hidden bridge semantic foundation applied."
Write-Host "Renderer/public route changes: none."

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = "$(Get-Location);$(Join-Path (Get-Location) 'tests')"

  pytest -q `
    ".\tests\test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  python ".\audit_phase144_6_r5_43_7.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
