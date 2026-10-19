$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$Package;$Root"
python -m pytest -q "$Package/tests/test_recover.py"
if ($LASTEXITCODE -ne 0) { throw 'Package safety tests failed' }
python "$Package/recover.py" --root "$Root"
if ($LASTEXITCODE -ne 0) { throw 'Recovery runner failed' }
Write-Host 'Historical helper recovery checked. No full pytest performed.'
