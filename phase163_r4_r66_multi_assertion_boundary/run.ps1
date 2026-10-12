$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q "$PSScriptRoot/tests/test_phase163_r4_r66_multi_assertion_boundary.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot/phase163_r4_r66_multi_assertion_boundary.py" --r65 "$root/phase163_r4_r65_output/review_packets.json" --output "$root/phase163_r4_r66_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R4-R66 read-only editorial boundary report complete. Full pytest not run."
