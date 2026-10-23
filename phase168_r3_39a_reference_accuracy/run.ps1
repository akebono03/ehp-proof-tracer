$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
python ".\phase168_r3_39a_reference_accuracy\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'Patch failed; pytest not run' }
python -m pytest -q ".\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py"
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'R3-39A focused reference accuracy complete. Full suite NOT run.'
