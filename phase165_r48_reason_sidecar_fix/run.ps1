$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Old = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$PSScriptRoot$([IO.Path]::PathSeparator)$Old" } else { "$Root$([IO.Path]::PathSeparator)$PSScriptRoot" }
  python (Join-Path $PSScriptRoot "install.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q (Join-Path $PSScriptRoot "test_r48_reason_sidecar.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally { $env:PYTHONPATH = $Old }
Write-Host "R48 targeted tests passed; full pytest NOT run."
