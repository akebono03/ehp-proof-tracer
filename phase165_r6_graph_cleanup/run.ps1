$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
python -m pytest -q "$folder\tests\test_cleanup.py"
if ($LASTEXITCODE -ne 0) { throw 'Graph cleanup tests failed' }
python "$folder\cleanup.py" --root "$root" --apply
if ($LASTEXITCODE -ne 0) { throw 'Graph cleanup failed' }
Write-Host 'Full pytest NOT run. Phase closure PENDING.'
