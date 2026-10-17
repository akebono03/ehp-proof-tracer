$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase165_rule_identity_r7.audit
  if ($LASTEXITCODE -ne 0) { throw 'R7 audit failed' }
  python -m pytest -q phase165_rule_identity_r7/test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'R7 targeted tests failed' }
  Write-Host 'R7 read-only review completed; full pytest NOT run.'
} finally {
  Pop-Location
}
