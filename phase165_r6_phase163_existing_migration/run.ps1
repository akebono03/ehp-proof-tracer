$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 source guard or patch failed' }
python -m pytest -q tests/test_phase163_r4_r11_literature_registration.py tests/test_phase163_r4_r12_literature_registration.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 targeted pytest failed' }
Write-Host 'Phase163 original 16 targeted tests PASS; full suite NOT run'
