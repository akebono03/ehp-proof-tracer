$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
$files = @(
  "phase162_validated_proof_presentation.py",
  "tests\test_phase162_r5_6_repair4_fixed_statement_reuse.py"
)
foreach ($file in $files) {
  $source = Join-Path (Join-Path $PSScriptRoot "files") $file
  $target = Join-Path (Get-Location) $file
  if (Test-Path $target) {
    Copy-Item $target ($target + ".phase162_r5_6_repair4.bak") -Force
  }
  $directory = Split-Path $target -Parent
  if (!(Test-Path $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
  Copy-Item $source $target -Force
  Write-Host "Updated: $file"
}
$tests = @(
  "tests/test_phase162_r2_validated_proof_presentation.py",
  "tests/test_phase162_r3_2_reference_display.py",
  "tests/test_phase162_r5_5_proof_narrative_composition.py",
  "tests/test_phase162_r5_6_proof_relevance_reference_attribution.py",
  "tests/test_phase162_r5_6_repair2_direct_reference_attribution.py",
  "tests/test_phase162_r5_6_repair3_reference_application_prose.py",
  "tests/test_phase162_r5_6_repair4_fixed_statement_reuse.py",
  "tests/test_phase161_r7_premise_provenance_validation.py"
)
python -B -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R5-6 Repair 4 focused tests complete. Full suite not run."
