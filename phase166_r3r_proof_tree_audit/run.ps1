$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$project;$bundle"
python -m pytest -q "$bundle/test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$bundle/audit.py"
exit $LASTEXITCODE
