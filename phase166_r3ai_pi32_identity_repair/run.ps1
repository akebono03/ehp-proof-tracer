$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$dir = Join-Path $repo "phase166_r3ai_pi32_identity_repair"
python (Join-Path $dir "apply.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $dir "tests/test_pi32_recovery.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $repo "phase166_r3af_goal_source/tests/test_r3af.py") (Join-Path $repo "phase166_r3ai_db_goal_priority/tests/test_r3ai.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Targeted regression PASS; full pytest NOT run."
