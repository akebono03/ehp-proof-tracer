$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$source = Join-Path $PSScriptRoot "files"
foreach ($relative in @(
  "phase162_validated_proof_presentation.py",
  "tests\test_phase162_r2_validated_proof_presentation.py",
  "tests\test_phase162_r5_4_iterated_suspension_structural_rendering.py"
)) {
  $target = Join-Path $root $relative
  if (Test-Path $target) { Copy-Item $target "$target.phase162_r5_4.bak" -Force }
  Copy-Item (Join-Path $source $relative) $target -Force
  Write-Host "Updated: $relative"
}
Push-Location $root
try {
  python -B -m pytest -q `
    tests/test_phase162_r2_validated_proof_presentation.py `
    tests/test_phase162_r3_2_reference_display.py `
    tests/test_phase162_r4_narrative_refinement.py `
    tests/test_phase162_r5_web_integration.py `
    tests/test_phase162_r5_2_general_reference_schema.py `
    tests/test_phase162_r5_3_reference_application_separation.py `
    tests/test_phase162_r5_4_iterated_suspension_structural_rendering.py `
    tests/test_phase161_r7_premise_provenance_validation.py
  if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
  Write-Host "Phase 162 R5-4 focused tests complete. Full suite not run."
} finally { Pop-Location }
