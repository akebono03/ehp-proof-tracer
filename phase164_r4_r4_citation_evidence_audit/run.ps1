$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project

$Required = @(
  'phase164_r4_r1_source_crosswalk.py',
  'phase164_r4_r2_semantic_structure.py',
  'phase164_r4_r3_independent_semantic_audit.py',
  'phase163_r4_r94_output/manifest.json',
  'tests/test_phase164_r4_r3_independent_semantic_audit.py',
  'tests/test_phase164_r4_r1_source_crosswalk.py'
)
foreach ($item in $Required) {
  if (-not (Test-Path (Join-Path $Project $item))) {
    throw "Missing R4-R4 prerequisite: $item"
  }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r4_citation_evidence_audit.py') (Join-Path $Project 'phase164_r4_r4_citation_evidence_audit.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests/test_phase164_r4_r4_citation_evidence_audit.py') (Join-Path $Project 'tests/test_phase164_r4_r4_citation_evidence_audit.py') -Force

python -B -m pytest -q `
  tests/test_phase164_r4_r4_citation_evidence_audit.py `
  tests/test_phase164_r4_r3_independent_semantic_audit.py `
  tests/test_phase164_r4_r1_source_crosswalk.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R4 targeted tests failed' }

python -B -m phase164_r4_r4_citation_evidence_audit `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r4_output'
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R4 audit execution failed' }
Write-Output 'Phase 164 R4-R4 evidence audit completed. Full pytest NOT run.'
