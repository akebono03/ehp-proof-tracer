$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$project;$package"
python -m pytest -q "$package/test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package/audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
