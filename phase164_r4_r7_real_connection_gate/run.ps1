$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'phase164_r2_citation_eligibility.py',
  'phase164_r3_registry_search_connection.py',
  'phase164_r4_r1_source_crosswalk.py',
  'phase164_r4_r3_independent_semantic_audit.py',
  'phase164_r4_r6_typed_binding.py',
  'phase163_r4_r94_output\manifest.json',
  'tests\test_phase59_n3_ehp_chain.py'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) {
    throw "Missing prerequisite: $File"
  }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r7_real_connection_gate.py') (Join-Path $Project 'phase164_r4_r7_real_connection_gate.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r4_r7_real_connection_gate.py') (Join-Path $Project 'tests\test_phase164_r4_r7_real_connection_gate.py') -Force
python -B -m pytest -q `
  tests/test_phase164_r4_r7_real_connection_gate.py `
  tests/test_phase164_r4_r6_typed_binding.py `
  tests/test_phase164_r3_registry_search_connection.py `
  tests/test_phase164_r2_citation_eligibility.py `
  tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R7 targeted pytest failed' }
python -B -m phase164_r4_r7_real_connection_gate `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r7_output'
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R7 gate audit failed' }
Write-Output 'Phase 164 R4-R7 connection gate audit completed. Full pytest NOT run.'
