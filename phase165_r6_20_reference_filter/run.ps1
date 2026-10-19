$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python "$PSScriptRoot\apply.py"
exit $LASTEXITCODE
