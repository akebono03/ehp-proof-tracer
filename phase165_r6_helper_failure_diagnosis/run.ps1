$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$Package;$Root"
python -m pytest -q "$Package/tests/test_diagnose.py"
if ($LASTEXITCODE -ne 0) { throw 'Safety tests failed' }
python "$Package/diagnose.py" --root "$Root"
if ($LASTEXITCODE -ne 0) { throw 'Cannot read failed helper recovery report' }
Write-Host 'Read-only diagnosis completed. No project tests, collection, or full pytest run.'
