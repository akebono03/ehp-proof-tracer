$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$py = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $py) { throw "python command is not available" }
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_installer.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R27-R43 targeted tests passed; full pytest NOT run."
