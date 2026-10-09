$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B "$ScriptDir\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q "$ScriptDir\test_r10_r4.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R10-R4 focused tests passed. Whole suite not run."
