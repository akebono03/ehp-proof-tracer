$ErrorActionPreference = 'Stop'
$phase = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $phase
Set-Location $root
python "$phase\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$phase\test_patch.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'R27-R26 targeted tests passed; full pytest NOT run.'
