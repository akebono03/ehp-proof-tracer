$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $root "phase162_validated_proof_presentation.py"))) { throw "Run from repository root" }
$targets = @(
    "phase162_validated_proof_presentation.py",
    "tests\test_phase162_r5_6_repair5_reference_component_boundary.py"
)
foreach ($target in $targets) {
    $src = Join-Path (Join-Path $package "files") $target
    $dst = Join-Path $root $target
    $parent = Split-Path -Parent $dst
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    if (Test-Path $dst) { Copy-Item $dst "$dst.phase162_r5_6_repair5.bak" -Force }
    Copy-Item $src $dst -Force
    Write-Host "Updated: $target"
}
$env:PYTHONPATH = $root
python -B -m pytest -q `
    tests/test_phase162_r5_6_repair5_reference_component_boundary.py `
    tests/test_phase162_r5_6_repair4_fixed_statement_reuse.py `
    tests/test_phase162_r5_6_repair3_reference_application_prose.py `
    tests/test_phase162_r5_6_repair2_direct_reference_attribution.py `
    tests/test_phase162_r5_6_proof_relevance_reference_attribution.py `
    tests/test_phase162_r3_2_reference_display.py `
    tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Phase 162 R5-6 Repair 5 focused tests complete. Full suite not run."
