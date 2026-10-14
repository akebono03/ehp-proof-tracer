$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $PSScriptRoot 'test_installer.py') (Join-Path $PSScriptRoot 'test_patch.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R33 targeted tests passed; full pytest NOT run.'
