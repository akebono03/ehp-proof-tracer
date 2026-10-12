$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B ".\phase164_r5_r3_math_punctuation\apply_patch.py"
if ($LASTEXITCODE -ne 0) { throw 'Web parser patch failed' }
python -B -m pytest -q tests/test_phase164_r5_r3_math_punctuation.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R3 targeted tests failed' }
Write-Host 'Phase 164 R5-R3 shared math punctuation fixed. Full pytest NOT run.'
