$ErrorActionPreference = 'Stop'
$repository = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = @(
  'toda_general_reference_schema.py',
  'phase162_validated_proof_presentation.py',
  'tests\test_phase162_r2_validated_proof_presentation.py',
  'tests\test_phase162_r3_2_reference_display.py',
  'tests\test_phase162_r5_2_general_reference_schema.py'
)
foreach ($relative in $files) {
  $source = Join-Path $package ('files\' + $relative)
  $target = Join-Path $repository $relative
  if (!(Test-Path $source)) { throw "Missing source file: $source" }
  $parent = Split-Path -Parent $target
  New-Item -ItemType Directory -Path $parent -Force | Out-Null
  if (Test-Path $target) { Copy-Item $target ($target + '.phase162_r5_2.bak') -Force }
  Copy-Item $source $target -Force
  Write-Host "Updated: $relative"
}
python -B -m pytest -q tests/test_phase162_r5_2_general_reference_schema.py tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase162_r4_narrative_refinement.py tests/test_phase162_r5_web_integration.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Phase 162 R5-2 focused tests complete. Full suite not run.'
