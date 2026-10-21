$ErrorActionPreference = "Stop"
python ".\phase166_r3ai_zero_search_connection\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase166_r3ai_zero_search_connection\tests\test_zero_search.py" ".\phase166_r3ai_zero_goal_support\tests\test_zero_goals.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Targeted pytest PASS; full pytest NOT run."
