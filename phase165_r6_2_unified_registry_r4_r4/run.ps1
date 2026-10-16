$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  python -m pytest -q (Join-Path $PSScriptRoot 'test_r4_r4.py')
  if ($LASTEXITCODE -ne 0) { throw 'Patch unit tests failed' }
  python (Join-Path $PSScriptRoot 'r4_r4_patch.py') --root $root
  if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
  python -m pytest -q (Join-Path $PSScriptRoot 'test_r4_r4_integration.py') tests/test_phase165_r8_rule_provider.py
  if ($LASTEXITCODE -ne 0) { throw 'Targeted regression failed' }
  Write-Output 'R4-4 installed; no full pytest run.'
} finally { Pop-Location }
