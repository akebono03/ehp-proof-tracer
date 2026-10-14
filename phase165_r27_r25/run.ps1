$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_installer.py" "$PSScriptRoot\test_patch.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R25 targeted checks passed; full pytest NOT run.'
