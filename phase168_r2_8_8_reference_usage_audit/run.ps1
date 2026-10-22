$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  python -m pytest -q --import-mode=importlib .\phase168_r2_8_8_reference_usage_audit\tests\test_phase168_r2_8_8_reference_usage_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
  python -m phase168_r2_8_8_reference_usage_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
} finally { Pop-Location }
