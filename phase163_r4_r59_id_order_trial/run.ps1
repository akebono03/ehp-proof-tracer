$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$readiness = Join-Path $root 'phase163_r4_r58_output\readiness.json'
if (-not (Test-Path $readiness)) { throw "Missing R4-R58 input: $readiness" }
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r59_id_order_trial\tests\test_phase163_r4_r59_id_order_trial.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-R59 focused pytest failed.' }
python '.\phase163_r4_r59_id_order_trial\phase163_r4_r59_id_order_trial.py' --readiness $readiness --output '.\phase163_r4_r59_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R59 audit failed.' }
