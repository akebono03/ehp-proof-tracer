$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Original = $env:PYTHONPATH
try {
  $env:PYTHONPATH = "$Root$([IO.Path]::PathSeparator)$PSScriptRoot"
  python -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python (Join-Path $PSScriptRoot 'audit.py')
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
  $env:PYTHONPATH = $Original
}
Write-Host 'R45 ProofStep inference audit complete; full pytest NOT run.'
