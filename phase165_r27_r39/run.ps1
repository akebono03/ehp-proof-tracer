$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$runner = Join-Path $PSScriptRoot 'apply.py'
python $runner $project
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $PSScriptRoot 'test_installer.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R39 targeted tests passed; full pytest NOT run.'
