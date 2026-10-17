$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase165_rule_duplicate_review_r6.audit
  if ($LASTEXITCODE -ne 0) { throw 'R6 audit failed' }
  python -m pytest -q phase165_rule_duplicate_review_r6/test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'R6 targeted tests failed' }
  Write-Host 'R6 reviewed five R5 candidates; no production changes; full pytest NOT run.'
} finally {
  Pop-Location
}
