$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
python ".\phase166_r3ai_zero_goal_support\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase166_r3ai_zero_goal_support\tests\test_zero_goals.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase166_r3ai_pi32_identity_repair\tests\test_pi32_recovery.py" ".\phase166_r3ai_db_goal_priority\tests\test_r3ai.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Targeted tests PASS; full pytest NOT run."
