$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $root "phase162_web_narrative_integration.py"))) { throw "Run from Phase 162 R5 repository root." }
$relative = "tests/test_phase162_r3_2_reference_display.py"
$source = Join-Path (Join-Path $package "files") $relative
$target = Join-Path $root $relative
$backup = Join-Path $package "backup/tests/test_phase162_r3_2_reference_display.py"
if (-not (Test-Path $target)) { throw "Missing target: $target" }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backup) | Out-Null
Copy-Item -Force $target $backup
Copy-Item -Force $source $target
Write-Host "Updated: $relative"
python -B -m pytest -q tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase162_r4_narrative_refinement.py tests/test_phase162_r5_web_integration.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R5 repair2 focused tests complete. Full suite not run."
