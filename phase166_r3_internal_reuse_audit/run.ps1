$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python -m phase166_r3_internal_reuse_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R3 internal audit failed' }
  python -m pytest -q phase166_r3_internal_reuse_audit/test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'R3 internal targeted tests failed' }
  Write-Host 'R3 internal proof reuse audit PASS (inspection only); full pytest NOT run.'
} finally {
  Pop-Location
}
