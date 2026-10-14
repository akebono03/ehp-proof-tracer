$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q test_phase165_r56_common_renderer.py test_phase165_r55_nk_only_goal.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R56 targeted tests passed; restart Flask. Full pytest NOT run.'
