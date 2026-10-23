$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Project
try {
  python -m phase168_r3_39c_source_leaf_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'Audit command failed.' }
  python -m pytest -q phase168_r3_39c_source_leaf_audit/tests/test_phase168_r3_39c_source_leaf_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed.' }
  Write-Host 'R3-39C source-leaf diagnostic complete. Full suite NOT run.'
} finally {
  Pop-Location
}
