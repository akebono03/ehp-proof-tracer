$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$source = Join-Path $PSScriptRoot 'files\tests'
$targets = @(
  'test_phase162_r3_2_reference_display.py',
  'test_phase162_r5_6_proof_relevance_reference_attribution.py',
  'test_phase162_r5_6_repair4_fixed_statement_reuse.py'
)
foreach ($filename in $targets) {
  $destination = Join-Path $root ('tests\' + $filename)
  if (-not (Test-Path $destination)) { throw ('Missing target: ' + $destination) }
  Copy-Item $destination ($destination + '.phase162_r5_6_repair4_test.bak') -Force
  Copy-Item (Join-Path $source $filename) $destination -Force
  Write-Host ('Updated: tests\' + $filename)
}
$tests = @(
  'tests/test_phase162_r3_2_reference_display.py',
  'tests/test_phase162_r5_6_proof_relevance_reference_attribution.py',
  'tests/test_phase162_r5_6_repair4_fixed_statement_reuse.py',
  'tests/test_phase162_r5_6_repair3_reference_application_prose.py',
  'tests/test_phase162_r5_6_repair2_direct_reference_attribution.py',
  'tests/test_phase162_r5_5_proof_narrative_composition.py',
  'tests/test_phase162_r2_validated_proof_presentation.py',
  'tests/test_phase161_r7_premise_provenance_validation.py'
)
python -B -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Phase 162 R5-6 Repair 4 test contract focused tests complete. Full suite not run.'
