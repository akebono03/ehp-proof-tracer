$ErrorActionPreference = "Stop"
$Project = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$Package;$Project"
python -m pytest -q "$Package\tests\test_repair.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$Package\repair.py"
exit $LASTEXITCODE
