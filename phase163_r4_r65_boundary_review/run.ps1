$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q "$PSScriptRoot/tests/test_phase163_r4_r65_boundary_review.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot/phase163_r4_r65_boundary_review.py" --r64 "$root/phase163_r4_r64_output/split_proposals.json" --r63 "$root/phase163_r4_r63_output/source_boundaries.json" --output "$root/phase163_r4_r65_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R4-R65 read-only review packets generated. Full pytest not run."
