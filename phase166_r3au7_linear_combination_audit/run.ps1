$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $PackageDir
Set-Location $RepoDir
python ".\phase166_r3au7_linear_combination_audit\audit.py" --repo .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest ".\phase166_r3au7_linear_combination_audit\test_r3au7.py" -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R3-AU-7 targeted PASS; full pytest NOT run.'
