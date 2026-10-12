$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $ProjectRoot
$env:PYTHONPATH = $ProjectRoot
$Source = Join-Path $PSScriptRoot 'phase164_r4_real_registry_audit.py'
$Target = Join-Path $ProjectRoot 'phase164_r4_real_registry_audit.py'
$TestSource = Join-Path $PSScriptRoot 'tests\test_phase164_r4_real_registry_audit.py'
$TestTarget = Join-Path $ProjectRoot 'tests\test_phase164_r4_real_registry_audit.py'
$Required = @('phase164_r3_registry_search_connection.py', 'phase164_r2_citation_eligibility.py', 'phase163_r4_r94_output\manifest.json', 'phase162_validated_proof_presentation.py', 'phase161_r7_premise_provenance_validation.py')
foreach ($Item in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Item))) { throw "Missing required input: $Item" }
}
Copy-Item $Source $Target -Force
Copy-Item $TestSource $TestTarget -Force
python -B -m pytest -q `
  tests/test_phase164_r4_real_registry_audit.py `
  tests/test_phase164_r3_registry_search_connection.py `
  tests/test_phase164_r2_citation_eligibility.py `
  tests/test_phase161_r7_premise_provenance_validation.py `
  tests/test_phase161_r5_backward_proof_reconstruction.py
if ($LASTEXITCODE -ne 0) { throw "Phase 164 R4 targeted pytest failed: $LASTEXITCODE" }
@'
from pathlib import Path
from phase164_r4_real_registry_audit import audit_phase164_r4, write_phase164_r4_report
root = Path.cwd()
result = audit_phase164_r4(root / 'phase163_r4_r94_output' / 'manifest.json')
write_phase164_r4_report(result, root / 'phase164_r4_output')
print('Phase 164 R4 audit:', result.report['real_registry_r3_status'])
print('Baseline proof steps:', result.report['legacy_derived_step_count'])
print('Report:', root / 'phase164_r4_output' / 'report.md')
print('Full pytest NOT run; no existing production code changed.')
'@ | python -B -
if ($LASTEXITCODE -ne 0) { throw "Phase 164 R4 report failed: $LASTEXITCODE" }
