$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_installer.py" "$PSScriptRoot\test_patch.py"
exit $LASTEXITCODE
