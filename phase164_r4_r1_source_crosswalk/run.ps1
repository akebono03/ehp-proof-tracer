$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$env:PYTHONPATH = $Root
$Required = @(
  'phase163_r4_r94_output\manifest.json',
  'phase163_r4_r95_phase_closure\r95_phase_closure.py',
  'phase164_r4_real_registry_audit.py',
  'phase161_r7_premise_provenance_validation.py',
  'tests\test_phase59_n3_ehp_chain.py'
)
foreach ($Path in $Required) {
  if (-not (Test-Path (Join-Path $Root $Path))) { throw "Missing prerequisite: $Path" }
}
$ModuleSource = Join-Path $PSScriptRoot 'phase164_r4_r1_source_crosswalk.py'
$TestSource = Join-Path $PSScriptRoot 'tests\test_phase164_r4_r1_source_crosswalk.py'
Copy-Item $ModuleSource (Join-Path $Root 'phase164_r4_r1_source_crosswalk.py') -Force
Copy-Item $TestSource (Join-Path $Root 'tests\test_phase164_r4_r1_source_crosswalk.py') -Force
python -B -m pytest -q `
  tests/test_phase164_r4_r1_source_crosswalk.py `
  tests/test_phase164_r4_real_registry_audit.py `
  tests/test_phase164_r3_registry_search_connection.py `
  tests/test_phase164_r2_citation_eligibility.py
if ($LASTEXITCODE -ne 0) { throw 'Phase164 R4-R1 targeted pytest failed' }
python -B phase164_r4_r1_source_crosswalk.py `
  --manifest phase163_r4_r94_output/manifest.json `
  --output phase164_r4_r1_output
if ($LASTEXITCODE -ne 0) { throw 'Phase164 R4-R1 audit failed' }
Write-Host 'Phase 164 R4-R1 read-only audit finished. Full pytest NOT run.'
