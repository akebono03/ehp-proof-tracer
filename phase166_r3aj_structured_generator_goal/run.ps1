$ErrorActionPreference = "Stop"
python ".\phase166_r3aj_structured_generator_goal\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase166_r3aj_structured_generator_goal\tests\test_structured_generator.py" ".\phase166_r3ai_zero_goal_support\tests\test_zero_goals.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Targeted tests PASS; full pytest NOT run."
