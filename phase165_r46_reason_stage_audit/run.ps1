$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Old=$env:PYTHONPATH
try {
  $env:PYTHONPATH= if ($Old) { "$Root$([IO.Path]::PathSeparator)$PSScriptRoot$([IO.Path]::PathSeparator)$Old" } else { "$Root$([IO.Path]::PathSeparator)$PSScriptRoot" }
  python -m pytest -q (Join-Path $PSScriptRoot "test_audit.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python (Join-Path $PSScriptRoot "audit.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally { $env:PYTHONPATH=$Old }
Write-Host "Read-only R46 stage audit finished; full pytest NOT run."
