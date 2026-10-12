$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B '.\phase164_r5_r3_patch_guard_fix\apply_patch.py'
if ($LASTEXITCODE -ne 0) { throw 'Web parser patch failed' }
python -B -m pytest -q phase164_r5_r3_patch_guard_fix/tests/test_phase164_r5_r3_math_punctuation.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R3 targeted tests failed' }
Write-Host 'Phase 164 R5-R3 shared punctuation parser installed; full pytest NOT run.'
