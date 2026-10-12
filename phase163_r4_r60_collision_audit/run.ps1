$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$inputFile = Join-Path $root 'phase163_r4_r59_output\id_order_trial.json'
if (-not (Test-Path $inputFile)) { throw "Missing R4-R59 input: $inputFile" }
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r60_collision_audit\tests\test_phase163_r4_r60_collision_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-R60 focused pytest failed.' }
python '.\phase163_r4_r60_collision_audit\phase163_r4_r60_collision_audit.py' --order $inputFile --output '.\phase163_r4_r60_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R60 audit failed.' }
