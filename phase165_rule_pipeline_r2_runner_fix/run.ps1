$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m phase165_rule_pipeline_r2_runner_fix.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_rule_pipeline_r2_runner_fix\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Generic rule pipeline audit complete; full pytest NOT run.'
