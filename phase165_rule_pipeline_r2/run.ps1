$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase165_rule_pipeline_r2\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_rule_pipeline_r2\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Generic rule pipeline audit complete; full pytest NOT run.'
