$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = $PSScriptRoot
$source = Join-Path $package "files"
if (-not (Test-Path (Join-Path $root "phase161_r7_premise_provenance_validation.py"))) { throw "Run from the EHP Proof Tracer repository root." }
$items = @(
    "phase162_validated_proof_presentation.py",
    "tests\test_phase162_r2_validated_proof_presentation.py",
    "tests\test_phase162_r3_2_reference_display.py",
    "tests\test_phase162_r4_narrative_refinement.py"
)
foreach ($item in $items) {
    $relative = $item.Replace("\", [IO.Path]::DirectorySeparatorChar)
    $destination = Join-Path $root $relative
    $parent = Split-Path $destination -Parent
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    Copy-Item (Join-Path $source $relative) $destination -Force
    Write-Host "Updated: $destination"
}
python -B -m pytest -q tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase162_r4_narrative_refinement.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Phase 162 R4 focused tests failed" }
Write-Host "Phase 162 R4 focused tests complete. Full suite not run."
