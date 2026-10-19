$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'Retirement aborted without running tests' }
python -m pytest -q "$PSScriptRoot\test_phase103_retirement_guard.py"
if ($LASTEXITCODE -ne 0) { throw 'Retirement guard tests failed; see archived backup' }
Write-Host 'Phase103 archive guards PASS; full pytest NOT run'
