$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$crosswalk = Join-Path $root 'phase163_r4_r52_output\crosswalk.json'
$overlap = Join-Path $root 'phase163_r4_r53_output\overlap_audit.json'
$gate = Join-Path $root 'phase163_r4_r61_output\registration_gate.json'
foreach ($path in @($crosswalk, $overlap, $gate)) {
    if (-not (Test-Path $path)) { throw "Missing required input: $path" }
}
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r62_remaining_definitions\tests\test_phase163_r4_r62_remaining_definitions.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-R62 focused pytest failed.' }
python '.\phase163_r4_r62_remaining_definitions\phase163_r4_r62_remaining_definitions.py' --crosswalk $crosswalk --overlap $overlap --gate $gate --output '.\phase163_r4_r62_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R62 inventory failed.' }
