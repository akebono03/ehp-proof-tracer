$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python -m pytest -q phase163_r4_r80_registration_preflight/tests/test_phase163_r4_r80_registration_preflight.py
if ($LASTEXITCODE -ne 0) { throw "R80 focused pytest failed." }
python phase163_r4_r80_registration_preflight/phase163_r4_r80_registration_preflight.py
if ($LASTEXITCODE -ne 0) { throw "R80 preflight failed." }
