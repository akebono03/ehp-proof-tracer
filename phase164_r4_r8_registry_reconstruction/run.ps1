$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'phase164_r4_r6_typed_binding.py',
  'phase164_r4_r3_independent_semantic_audit.py',
  'phase164_r4_r1_source_crosswalk.py',
  'phase161_r7_premise_provenance_validation.py',
  'phase162_validated_proof_presentation.py',
  'phase163_r4_r94_output\manifest.json',
  'tests\test_phase59_n3_ehp_chain.py'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) {
    throw "Missing prerequisite: $File"
  }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r8_registry_reconstruction.py') (Join-Path $Project 'phase164_r4_r8_registry_reconstruction.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r4_r8_registry_reconstruction.py') (Join-Path $Project 'tests\test_phase164_r4_r8_registry_reconstruction.py') -Force
python -B -m pytest -q `
  tests/test_phase164_r4_r8_registry_reconstruction.py `
  tests/test_phase164_r4_r6_typed_binding.py `
  tests/test_phase164_r4_r3_independent_semantic_audit.py `
  tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R8 targeted tests failed' }
python -B -m phase164_r4_r8_registry_reconstruction `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r8_output'
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R8 reconstruction failed' }
Write-Output 'Phase 164 R4-R8 registry-backed pi5_3 reconstruction completed. Full pytest NOT run.'
