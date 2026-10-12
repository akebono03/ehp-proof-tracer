$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'phase164_r4_r1_source_crosswalk.py',
  'phase164_r4_r2_semantic_structure.py',
  'phase163_r4_r94_output\manifest.json',
  'tests\test_phase164_r4_r2_semantic_structure.py',
  'tests\test_phase59_n3_ehp_chain.py'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) {
    throw "Missing prerequisite: $File"
  }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r3_independent_semantic_audit.py') (Join-Path $Project 'phase164_r4_r3_independent_semantic_audit.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r4_r3_independent_semantic_audit.py') (Join-Path $Project 'tests\test_phase164_r4_r3_independent_semantic_audit.py') -Force
python -B -m pytest -q `
  tests/test_phase164_r4_r3_independent_semantic_audit.py `
  tests/test_phase164_r4_r2_semantic_structure.py `
  tests/test_phase164_r4_r1_source_crosswalk.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R3 targeted tests failed' }
python -B -m phase164_r4_r3_independent_semantic_audit `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r3_output'
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R3 audit failed' }
Write-Output 'Phase 164 R4-R3 symbolic-dimension repair audit completed. Full pytest NOT run.'
