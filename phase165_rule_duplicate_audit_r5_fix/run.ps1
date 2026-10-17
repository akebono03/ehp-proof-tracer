$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase165_rule_duplicate_audit_r5_fix.audit
  if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
  python -m pytest -q phase165_rule_duplicate_audit_r5_fix/test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
  Write-Host 'Active R8 duplicate audit passed; retired catalog NOT called; full pytest NOT run.'
} finally {
  Pop-Location
}
