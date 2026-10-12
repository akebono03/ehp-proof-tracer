$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project

$Required = @(
  'phase164_r4_r1_source_crosswalk.py',
  'phase164_r4_real_registry_audit.py',
  'phase163_r4_r94_output/manifest.json',
  'phase163_r4_r95_phase_closure/r95_phase_closure.py',
  'tests/test_phase59_n3_ehp_chain.py'
)
foreach ($file in $Required) {
  if (-not (Test-Path (Join-Path $Project $file))) {
    throw "Required dependency missing: $file"
  }
}

Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r2_semantic_structure.py') (Join-Path $Project 'phase164_r4_r2_semantic_structure.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests/test_phase164_r4_r2_semantic_structure.py') (Join-Path $Project 'tests/test_phase164_r4_r2_semantic_structure.py') -Force

python -B -m pytest -q `
  tests/test_phase164_r4_r2_semantic_structure.py `
  tests/test_phase164_r4_r1_source_crosswalk.py `
  tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R2 targeted pytest failed' }

python -B -m phase164_r4_r2_semantic_structure `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r2_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R2 audit failed' }
Write-Output 'Phase 164 R4-R2 read-only semantic-structure audit finished. Full pytest NOT run.'
