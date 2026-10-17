$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_adapter_removed.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'Pi43 group-specific adapter removed; targeted pytest passed; full pytest NOT run.'
