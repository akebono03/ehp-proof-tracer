$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$source = Join-Path $PSScriptRoot "files\tests"
$targets = @(
  "phase162_r5_6_reference_test_utils.py",
  "test_phase162_r2_validated_proof_presentation.py",
  "test_phase162_r3_2_reference_display.py",
  "test_phase162_r5_5_proof_narrative_composition.py"
)
if (-not (Test-Path (Join-Path $repo "phase162_validated_proof_presentation.py"))) {
  throw "Execute in the EHP Proof Tracer repository root."
}
foreach ($name in $targets) {
  $destination = Join-Path $repo ("tests\" + $name)
  $origin = Join-Path $source $name
  if (-not (Test-Path $origin)) { throw "Missing repair file: $origin" }
  if (Test-Path $destination) {
    Copy-Item $destination ($destination + ".phase162_r5_6_test_repair.bak") -Force
  }
  Copy-Item $origin $destination -Force
  Write-Host "Updated: tests\$name"
}
python -B -m pytest -q `
  tests/test_phase162_r2_validated_proof_presentation.py `
  tests/test_phase162_r3_2_reference_display.py `
  tests/test_phase162_r4_narrative_refinement.py `
  tests/test_phase162_r5_web_integration.py `
  tests/test_phase162_r5_2_general_reference_schema.py `
  tests/test_phase162_r5_3_reference_application_separation.py `
  tests/test_phase162_r5_4_iterated_suspension_structural_rendering.py `
  tests/test_phase162_r5_5_proof_narrative_composition.py `
  tests/test_phase162_r5_6_proof_relevance_reference_attribution.py `
  tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R5-6 attribution contract repair focused tests complete. Full suite not run."
