$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = Join-Path $package "files"
foreach ($relative in @(
    "tests\test_phase162_r2_validated_proof_presentation.py",
    "tests\test_phase162_r3_2_reference_display.py"
)) {
    $source = Join-Path $files $relative
    $target = Join-Path $root $relative
    if (!(Test-Path $target)) { throw "Expected previous R3-2 file missing: $target" }
    Copy-Item -LiteralPath $source -Destination $target -Force
    Write-Host "Updated: $target"
}
python -B -m pytest -q tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase162_r3_2_reference_display.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R3-2 test repair focused tests complete. Full suite not run."
