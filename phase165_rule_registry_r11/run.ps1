$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase165_rule_registry_r11.audit
  if ($LASTEXITCODE -ne 0) { throw 'R11 audit failed' }
  python -m pytest -q phase165_rule_registry_r11/test_audit.py tests/test_phase165_r8_rule_provider.py
  if ($LASTEXITCODE -ne 0) { throw 'R11 targeted pytest failed' }
  Write-Host 'R11 registry connection verified; targeted tests passed; full pytest NOT run.'
} finally {
  Pop-Location
}
