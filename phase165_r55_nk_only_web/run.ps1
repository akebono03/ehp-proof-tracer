$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q test_phase165_r55_nk_only_goal.py test_phase165_r54_explicit_web_goal.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R55 targeted tests passed. Restart Flask. Full pytest NOT run.'
