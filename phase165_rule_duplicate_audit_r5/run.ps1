$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase165_rule_duplicate_audit_r5.audit
  if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
  python -m pytest -q phase165_rule_duplicate_audit_r5/test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
  Write-Host 'Rule duplicate audit completed; full pytest NOT run.'
} finally {
  Pop-Location
}
