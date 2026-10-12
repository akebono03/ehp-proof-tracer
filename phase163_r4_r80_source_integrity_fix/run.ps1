$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python -m pytest -q phase163_r4_r80_source_integrity_fix/tests/test_phase163_r4_r80_registration_preflight.py
if ($LASTEXITCODE -ne 0) { throw "R80 source integrity focused pytest failed." }
python phase163_r4_r80_source_integrity_fix/phase163_r4_r80_registration_preflight.py
if ($LASTEXITCODE -ne 0) { throw "R80 source integrity preflight failed." }
