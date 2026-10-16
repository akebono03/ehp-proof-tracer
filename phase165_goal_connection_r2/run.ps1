$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase165_goal_connection_r2\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_goal_connection_r2\test_goal_connection.py" ".\tests\test_phase165_r3_recursive_search.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Goal connection targeted tests passed; full pytest NOT run.'
