$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
python -B "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q "$PSScriptRoot\tests"
exit $LASTEXITCODE
