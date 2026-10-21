$ErrorActionPreference = "Stop"
python ".\phase166_r3ak_public_target\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase166_r3ak_public_target\tests\test_public_target.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Targeted pytest PASS; full pytest NOT run."
