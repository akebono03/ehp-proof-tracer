$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path
python -m phase166_r3al_112_target_audit.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase166_r3al_112_target_audit\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Read-only targeted audit complete; full pytest NOT run."
