$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'web_group_proof.py',
  'phase164_r4_r8_registry_reconstruction.py',
  'phase164_r4_r6_typed_binding.py',
  'phase164_r4_r1_source_crosswalk.py',
  'phase162_pi5_3_web_replay.py',
  'phase162_validated_proof_presentation.py',
  'phase163_r4_r94_output\manifest.json'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) { throw "Missing prerequisite: $File" }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r5_web_registry_connection.py') (Join-Path $Project 'phase164_r5_web_registry_connection.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r5_web_registry_connection.py') (Join-Path $Project 'tests\test_phase164_r5_web_registry_connection.py') -Force
python -B (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 patch failed' }
python -B -m pytest -q `
  tests/test_phase164_r5_web_registry_connection.py `
  tests/test_phase164_r4_r8_registry_reconstruction.py `
  tests/test_phase164_r4_r6_typed_binding.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R5 targeted tests failed' }
Write-Output 'Phase 164 R5 Web registry-backed pi5_3 narrative connected. Full pytest NOT run.'
