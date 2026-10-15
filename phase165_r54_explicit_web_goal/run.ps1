$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q test_phase165_r54_explicit_web_goal.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R54 targeted tests passed. Restart Flask to see the form. Full pytest NOT run.'
