$ErrorActionPreference = 'Stop'
$Project = (Get-Location).Path
$Package = $PSScriptRoot
$Required = @(
  'unified_statement_registry.py',
  'phase163_r4_registry_bridge.py',
  'phase164_r2_citation_eligibility.py',
  'phase161_r5_backward_proof_reconstruction.py',
  'phase161_r7_premise_provenance_validation.py',
  'tests/test_phase161_r7_premise_provenance_validation.py'
)
foreach ($item in $Required) {
  if (-not (Test-Path (Join-Path $Project $item))) {
    throw "Required existing project file missing: $item"
  }
}
$Target = Join-Path $Project 'phase164_r3_registry_search_connection.py'
$TestTarget = Join-Path $Project 'tests/test_phase164_r3_registry_search_connection.py'
if (Test-Path $Target) { throw "Refusing to overwrite existing module: $Target" }
if (Test-Path $TestTarget) { throw "Refusing to overwrite existing test: $TestTarget" }
Copy-Item (Join-Path $Package 'phase164_r3_registry_search_connection.py') $Target
Copy-Item (Join-Path $Package 'tests/test_phase164_r3_registry_search_connection.py') $TestTarget
$env:PYTHONPATH = $Project
python -B -m pytest -q `
  tests/test_phase164_r3_registry_search_connection.py `
  tests/test_phase164_r2_citation_eligibility.py `
  tests/test_phase161_r5_backward_proof_reconstruction.py `
  tests/test_phase161_r7_premise_provenance_validation.py `
  tests/test_phase163_r3_registry_validation.py
if ($LASTEXITCODE -ne 0) { throw "Phase 164 R3 targeted pytest failed (exit $LASTEXITCODE)" }
Write-Output 'Phase 164 R3 targeted tests passed. Full pytest NOT run.'
