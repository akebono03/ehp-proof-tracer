$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
  python -m phase165_rule_identity_r8.audit
  if ($LASTEXITCODE -ne 0) { throw 'R8 audit failed' }
  python -m pytest -q phase165_rule_identity_r8/test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'R8 targeted pytest failed' }
  Write-Host 'Phase 165 R8 review passed; production unchanged; full pytest NOT run.'
} finally {
  Pop-Location
}
