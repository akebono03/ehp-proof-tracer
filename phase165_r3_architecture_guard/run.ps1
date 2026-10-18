$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r4_flask_bridge.py')) { throw 'Run from ehp_proof project root.' }
$root = (Get-Location).Path
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
python -m pytest -q "$PSScriptRoot\tests\test_phase165_r3_architecture_guard.py"
if ($LASTEXITCODE -ne 0) { throw 'R3 architecture guard failed. No project source modified.' }
python "$PSScriptRoot\check.py"
if ($LASTEXITCODE -ne 0) { throw 'R3 public snapshot verification failed. No project source modified.' }
Write-Host 'R3 targeted tests PASS. Full pytest NOT run. No production files modified.'
