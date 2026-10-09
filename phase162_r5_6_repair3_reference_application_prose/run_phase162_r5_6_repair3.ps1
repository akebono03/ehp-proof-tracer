$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $root "phase162_validated_proof_presentation.py"
$source = Join-Path $bundle "files\phase162_validated_proof_presentation.py"
if (!(Test-Path $target)) { throw "Run from repository root" }
Copy-Item $target ($target + ".phase162_r5_6_repair3.bak") -Force
Copy-Item $source $target -Force
Write-Host "Updated: phase162_validated_proof_presentation.py"
$testfile = Join-Path $root "tests\test_phase162_r5_6_repair3_reference_application_prose.py"
Copy-Item (Join-Path $bundle "files\tests\test_phase162_r5_6_repair3_reference_application_prose.py") $testfile -Force
Write-Host "Updated: tests\test_phase162_r5_6_repair3_reference_application_prose.py"
python -m pytest -q tests/test_phase162_r5_6_repair3_reference_application_prose.py tests/test_phase162_r5_6_repair2_direct_reference_attribution.py tests/test_phase162_r5_6_proof_relevance_reference_attribution.py tests/test_phase162_r5_5_proof_narrative_composition.py tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R5-6 Repair 3 focused tests complete. Full suite not run."
