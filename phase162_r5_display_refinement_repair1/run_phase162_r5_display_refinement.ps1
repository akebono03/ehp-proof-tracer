$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = @(
  "phase162_validated_proof_presentation.py",
  "tests/test_phase162_r4_narrative_refinement.py",
  "tests/test_phase162_r5_web_integration.py"
)
if (-not (Test-Path (Join-Path $root "phase161_r7_premise_provenance_validation.py"))) {
  throw "Run from the EHP Proof Tracer repository root."
}
if (-not (Test-Path (Join-Path $root "phase162_web_narrative_integration.py"))) {
  throw "Apply Phase 162 R5 first."
}
$backup = Join-Path $package "backup"
foreach ($file in $files) {
  $src = Join-Path (Join-Path $package "files") $file
  $dst = Join-Path $root $file
  if (-not (Test-Path $dst)) { throw "Missing target: $dst" }
  $back = Join-Path $backup $file
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $back) | Out-Null
  Copy-Item -Force $dst $back
  Copy-Item -Force $src $dst
  Write-Host "Updated: $file"
}
python -B -m pytest -q tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase162_r4_narrative_refinement.py tests/test_phase162_r5_web_integration.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R5 display refinement focused tests complete. Full suite not run."
