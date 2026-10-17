$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase165_rule_registry_r11_fix.audit
  if ($LASTEXITCODE -ne 0) { throw 'R11 repaired audit failed' }
  python -m pytest -q phase165_rule_registry_r11_fix/test_audit.py tests/test_phase165_r8_rule_provider.py
  if ($LASTEXITCODE -ne 0) { throw 'R11 repaired targeted pytest failed' }
  Write-Host 'R11 shared discovery alias checks passed; full pytest NOT run.'
} finally { Pop-Location }
