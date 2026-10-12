$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$readiness = Join-Path $root 'phase163_r4_r58_output\readiness.json'
$order = Join-Path $root 'phase163_r4_r59_output\id_order_trial.json'
$collision = Join-Path $root 'phase163_r4_r60_output\collision_audit.json'
foreach ($file in @($readiness, $order, $collision)) {
    if (-not (Test-Path $file)) { throw "Missing required input: $file" }
}
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r61_registration_gate\tests\test_phase163_r4_r61_registration_gate.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-R61 focused pytest failed.' }
python '.\phase163_r4_r61_registration_gate\phase163_r4_r61_registration_gate.py' --readiness $readiness --order $order --collision $collision --output '.\phase163_r4_r61_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R61 registration gate failed.' }
