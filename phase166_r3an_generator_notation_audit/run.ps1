$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  # Run as a module so the repository root is on Python's import path.
  python -m phase166_r3an_generator_notation_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
  python -m pytest -q .\phase166_r3an_generator_notation_audit\test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
  Write-Host 'Read-only notation audit completed; full pytest NOT run.'
} finally {
  Pop-Location
}
