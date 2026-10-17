$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m phase165_rule_registry_audit_r3.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q '.\phase165_rule_registry_audit_r3\test_audit.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Rule registry R3 read-only audit complete; full pytest NOT run.'
