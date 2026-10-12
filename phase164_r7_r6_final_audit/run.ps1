$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$scriptDir;$project"
python -m pytest -q "$scriptDir/test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R7-R6 audit unit tests failed' }
python "$scriptDir/audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R7-R6 structural audit failed; inspect output' }
Write-Host 'Phase 164 R7-R6 read-only audit completed; full pytest NOT run.'
